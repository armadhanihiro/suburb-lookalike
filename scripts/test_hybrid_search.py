from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.profiles import generate_profiles
from engine.text_embed import load_or_create_embeddings
from engine.fusion import fuse_vectors
from engine.similarity import find_similar_suburbs


def main():
    client = get_bigquery_client()

    df, X_numeric, scaler = load_suburb_data(client)

    # Test first 20 suburbs
    df_sample = df.head(20).copy()
    X_numeric_sample = X_numeric[:20]

    profiles = generate_profiles(df_sample)

    X_text_sample = load_or_create_embeddings(
        profiles,
        cache_path="cache/test_hybrid_embeddings.npy",
    )

    X_hybrid = fuse_vectors(
        X_numeric_sample,
        X_text_sample,
        alpha=0.4,
    )

    reference_idx = 0

    numeric_results = find_similar_suburbs(
        X_numeric_sample,
        reference_idx,
        top_n=5,
    )

    hybrid_results = find_similar_suburbs(
        X_hybrid,
        reference_idx,
        top_n=5,
    )

    print("\nReference suburb:")
    print(df_sample.iloc[reference_idx][["sa2_code", "sa2_name", "state"]])

    print("\nNumeric-only results:")
    for rank, item in enumerate(numeric_results, start=1):
        suburb = df_sample.iloc[item["index"]]
        print(rank, suburb["sa2_name"], suburb["state"], round(item["similarity"], 4))

    print("\nHybrid results:")
    for rank, item in enumerate(hybrid_results, start=1):
        suburb = df_sample.iloc[item["index"]]
        print(rank, suburb["sa2_name"], suburb["state"], round(item["similarity"], 4))


if __name__ == "__main__":
    main()