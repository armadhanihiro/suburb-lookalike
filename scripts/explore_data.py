from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data, KPI_COLS, METADATA_COLS

TABLE_NAME = "demografy.prod_tables.a_master_view"

def main():
    client = get_bigquery_client()
    query = f"""
        SELECT
            {", ".join(METADATA_COLS)},
            {", ".join(KPI_COLS)}
        FROM `{TABLE_NAME}`
    """

    raw_df = client.query(query).to_dataframe()

    print("\n=== RAW DATA OVERVIEW ===")
    print("Total rows / suburbs:", len(raw_df))
    print("Columns:", list(raw_df.columns))

    print("\n=== METADATA NULL CHECK ===")
    print(raw_df[METADATA_COLS].isnull().sum())

    print("\n=== KPI RAW NULL CHECK ===")
    print(raw_df[KPI_COLS].isnull().sum())

    print("\n=== ROWS WITH AT LEAST ONE KPI NULL ===")
    rows_with_null = raw_df[raw_df[KPI_COLS].isnull().any(axis=1)]
    print("Count:", len(rows_with_null))
    print(rows_with_null[METADATA_COLS + KPI_COLS].head(20))

    print("\n=== UNIQUE IDENTIFIER CHECK ===")
    print("Duplicate sa2_code count:", raw_df["sa2_code"].duplicated().sum())

    print("\n=== DUPLICATE SA2 NAME CHECK ===")
    duplicate_names = raw_df[raw_df.duplicated(subset=["sa2_name"], keep=False)]
    print("Duplicate sa2_name rows:", len(duplicate_names))
    print(duplicate_names[["sa2_code", "sa2_name", "state"]].head(30))

    print("\n=== DUPLICATE SA2 NAME + STATE CHECK ===")
    duplicate_name_state = raw_df[
        raw_df.duplicated(subset=["sa2_name", "state"], keep=False)
    ]
    print("Duplicate sa2_name + state rows:", len(duplicate_name_state))
    print(duplicate_name_state[["sa2_code", "sa2_name", "state"]].head(30))

    print("\n=== KPI RANGES RAW DATA ===")
    for col in KPI_COLS:
        print(
            col,
            "min:", raw_df[col].min(),
            "max:", raw_df[col].max(),
            "median:", raw_df[col].median(),
            "mean:", raw_df[col].mean(),
        )

    print("\n=== AFTER FEATURE PIPELINE ===")
    processed_df, X, scaler = load_suburb_data(client)

    print("Processed rows:", len(processed_df))
    print("Feature matrix shape:", X.shape)

    print("\n=== KPI NULL CHECK AFTER MEDIAN IMPUTATION ===")
    print(processed_df[KPI_COLS].isnull().sum())

    print("\n=== STANDARDIZED MATRIX QUICK CHECK ===")
    print("Mean per feature:")
    print(X.mean(axis=0))

    print("\nStandard deviation per feature:")
    print(X.std(axis=0))


if __name__ == "__main__":
    main()