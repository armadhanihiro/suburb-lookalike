from sklearn.preprocessing import StandardScaler

METADATA_COLS = [
    "sa2_code",
    "sa2_name",
    "sa3_code",
    "sa3_name",
    "sa4_code",
    "sa4_name",
    "gcca_code",
    "gcca_name",
    "state",
    "area",
    "population",
]


KPI_COLS = [
    f"kpi_{i}_val" for i in range(1, 11)
]


def load_suburb_data(client):
    query = f"""
        SELECT
            {", ".join(METADATA_COLS)},
            {", ".join(KPI_COLS)}
        FROM `demografy.prod_tables.a_master_view`
    """

    df = client.query(query).to_dataframe()

    # Handle missing KPI values
    df[KPI_COLS] = df[KPI_COLS].fillna(df[KPI_COLS].median())

    # Standardise KPI values
    scaler = StandardScaler()

    X = scaler.fit_transform(df[KPI_COLS])

    return df, X, scaler