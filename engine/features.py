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

MIN_AVAILABLE_KPIS = 5


def load_suburb_data(client):
    query = f"""
        SELECT
            {", ".join(METADATA_COLS)},
            {", ".join(KPI_COLS)}
        FROM `demografy.prod_tables.a_master_view`
    """

    df = client.query(query).to_dataframe()

    missing_counts = df[KPI_COLS].isna().sum(axis=1)

    df["missing_kpi_count"] = missing_counts
    df["missing_kpi_ratio"] = missing_counts / len(KPI_COLS)
    df["is_low_data_quality"] = missing_counts > (len(KPI_COLS) - MIN_AVAILABLE_KPIS)

    before_count = len(df)

    df = df[~df["is_low_data_quality"]].copy()

    # Flag remote / low-population outliers.
    # We do not remove them because they may still be valid suburbs,
    # but downstream UI/evaluation can treat them as special cases.
    population_threshold = df["population"].quantile(0.05)
    area_threshold = df["area"].quantile(0.95)

    df["is_remote_outlier"] = ((df["population"] <= population_threshold) & (df["area"] >= area_threshold))

    removed_count = before_count - len(df)

    if removed_count > 0:
        print(
            f"Removed {removed_count} suburbs with fewer than "
            f"{MIN_AVAILABLE_KPIS} available KPI values."
        )

    sa4_medians = df.groupby("sa4_code")[KPI_COLS].transform("median")

    df[KPI_COLS] = df[KPI_COLS].fillna(sa4_medians)

    df[KPI_COLS] = df[KPI_COLS].fillna(df[KPI_COLS].median())

    scaler = StandardScaler()

    X = scaler.fit_transform(df[KPI_COLS])

    duplicate_count = df["display_name"].duplicated().sum() if "display_name" in df.columns else 0

    if duplicate_count > 0:
        print(f"Warning: found {duplicate_count} duplicate display names.")

    return df, X, scaler