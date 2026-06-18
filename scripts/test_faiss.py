from db.bigquery_client import get_bigquery_client

from engine.features import load_suburb_data
from engine.text_embed import load_or_create_embeddings
from engine.fusion import fuse_vectors
from engine.index import (
    build_faiss_index,
    save_index,
    load_index,
    search_index,
)


def main():
    client = get_bigquery_client()
    df, X_numeric, _ = load_suburb_data(client)

    X_text = load_or_create_embeddings(
        profiles=[],
        cache_path="cache/suburb_embeddings.npy",
    )


    X_hybrid = fuse_vectors( X_numeric, X_text, alpha=0.4,)
    index = build_faiss_index(X_hybrid)
    save_index(index)
    loaded_index = load_index()
    reference_idx = 0

    scores, indices = search_index(
        loaded_index,
        X_hybrid[reference_idx].reshape(1, -1),
        top_n=11,
    )

    print("\nReference suburb:")
    print(df.iloc[reference_idx][["sa2_name", "state"]])
    print("\nFAISS results:")

    rank = 1
    for score, idx in zip(scores, indices):
        if idx == reference_idx:
            continue
        suburb = df.iloc[idx]
        print(rank, suburb["sa2_name"], suburb["state"], round(float(score), 4),)
        rank += 1

if __name__ == "__main__":
    main()