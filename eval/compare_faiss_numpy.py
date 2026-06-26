from db.bigquery_client import get_bigquery_client

from engine.features import load_suburb_data
from engine.fusion import fuse_vectors
from engine.text_embed import load_or_create_embeddings
from engine.similarity import find_similar_suburbs
from engine.index import build_faiss_index, search_index


def faiss_search(vectors, reference_idx, top_n=10):
    index = build_faiss_index(vectors)

    scores, indices = search_index(
        index,
        vectors[reference_idx].reshape(1, -1),
        top_n=top_n + 1,
    )

    results = []

    for score, idx in zip(scores, indices):
        idx = int(idx)

        if idx == reference_idx:
            continue

        results.append(
            {
                "index": idx,
                "similarity": float(score),
            }
        )

        if len(results) == top_n:
            break

    return results


def main():
    client = get_bigquery_client()
    df, x_numeric, _ = load_suburb_data(client)
    x_text = load_or_create_embeddings(
        profiles=[],
        cache_path="cache/suburb_embeddings.npy",
    )

    x_hybrid = fuse_vectors(
        x_numeric,
        x_text,
        alpha=0.4,
    )

    reference_indices = list(range(10))
    top_n = 10

    print("=== FAISS vs NumPy neighbour comparison ===")

    all_passed = True

    for reference_idx in reference_indices:
        numpy_results = find_similar_suburbs(
            x_hybrid,
            reference_idx,
            top_n=top_n,
        )

        faiss_results = faiss_search(
            x_hybrid,
            reference_idx,
            top_n=top_n,
        )

        numpy_neighbours = [
            item["index"]
            for item in numpy_results
        ]

        faiss_neighbours = [
            item["index"]
            for item in faiss_results
        ]

        reference = df.iloc[reference_idx]

        is_same = numpy_neighbours == faiss_neighbours

        print(
            f"\nReference {reference_idx}: "
            f"{reference['sa2_name']} - {reference['state']}"
        )

        print("NumPy:", numpy_neighbours)
        print("FAISS:", faiss_neighbours)
        print("Match:", is_same)

        if not is_same:
            all_passed = False

    if not all_passed:
        raise AssertionError(
            "FAISS and NumPy returned different neighbours."
        )

    print("\nAll FAISS results match NumPy baseline ✅")


if __name__ == "__main__":
    main()