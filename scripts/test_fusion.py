from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.profiles import generate_profiles
from engine.text_embed import load_or_create_embeddings
from engine.fusion import fuse_vectors


def main():
    client = get_bigquery_client()

    df, X_numeric, scaler = load_suburb_data(client)

    profiles = generate_profiles(df)

    sample_profiles = profiles[:5]
    sample_numeric = X_numeric[:5]

    X_text = load_or_create_embeddings(
        sample_profiles,
        cache_path="cache/test_embeddings.npy"
    )

    X_hybrid = fuse_vectors(
        sample_numeric,
        X_text,
        alpha=0.4
    )

    print("Numeric shape:", sample_numeric.shape)
    print("Text embedding shape:", X_text.shape)
    print("Hybrid shape:", X_hybrid.shape)

    print("First hybrid vector first 5 values:")
    print(X_hybrid[0][:5])


if __name__ == "__main__":
    main()