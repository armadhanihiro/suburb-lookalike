from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.profiles import generate_profiles
from engine.text_embed import load_or_create_embeddings


def main():
    client = get_bigquery_client()
    df, X_numeric, scaler = load_suburb_data(client)

    print("Total suburbs:", len(df))

    profiles = generate_profiles(df)
    embeddings = load_or_create_embeddings(
        profiles,
        cache_path="cache/suburb_embeddings.npy",
    )

    print("Embeddings shape:", embeddings.shape)


if __name__ == "__main__":
    main()