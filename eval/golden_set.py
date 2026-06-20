from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.fusion import fuse_vectors
from engine.text_embed import load_or_create_embeddings
from engine.similarity import find_similar_suburbs


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

    reference_indices = list(range(5))

    for reference_idx in reference_indices:
        reference = df.iloc[reference_idx]

        results = find_similar_suburbs(
            x_hybrid,
            reference_idx,
            top_n=10,
        )

        print("\nReference:")
        print(reference["sa2_name"], "-", reference["state"])

        print("Top matches:")
        for rank, item in enumerate(results, start=1):
            match = df.iloc[item["index"]]

            print(
                rank,
                match["sa2_name"],
                "-",
                match["state"],
                round(item["similarity"], 4),
            )


if __name__ == "__main__":
    main()