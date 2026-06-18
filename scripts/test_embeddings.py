from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.profiles import generate_profiles
from engine.text_embed import load_or_create_embeddings


def main():
    client = get_bigquery_client()

    df, X, scaler = load_suburb_data(client)

    profiles = generate_profiles(df)

    # test first 5
    sample_profiles = profiles[:5]

    embeddings = load_or_create_embeddings(
        sample_profiles,
        cache_path="cache/test_embeddings.npy"
    )

    print("Embeddings shape:", embeddings.shape)
    print("First vector first 5 values:", embeddings[0][:5])


if __name__ == "__main__":
    main()