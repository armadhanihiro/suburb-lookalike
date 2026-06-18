from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.text_embed import load_or_create_embeddings
from engine.fusion import fuse_vectors
from engine.similarity import find_similar_suburbs


def main():
    client = get_bigquery_client()
    df, X_numeric, scaler = load_suburb_data(client)

    X_text = load_or_create_embeddings(
        profiles=[],
        cache_path="cache/suburb_embeddings.npy",
    )

    X_hybrid = fuse_vectors(
        X_numeric,
        X_text,
        alpha=0.4,
    )

    reference_idx = 0
    results = find_similar_suburbs(
        X_hybrid,
        reference_idx,
        top_n=10,
    )

    print("\nReference suburb:")
    print(df.iloc[reference_idx][["sa2_code", "sa2_name", "state"]])

    print("\nHybrid similar suburbs:")
    for rank, item in enumerate(results, start=1):
        suburb = df.iloc[item["index"]]
        print(
            rank,
            suburb["sa2_name"],
            suburb["state"],
            round(item["similarity"], 4),
        )


if __name__ == "__main__":
    main()