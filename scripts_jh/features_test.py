# features_test.py
import pandas as pd
from sklearn.preprocessing import StandardScaler

KPI_COLS = [f"kpi_{i}_val" for i in range(1, 11)]

def load_suburb_data_test(client):
    """
    改进版 load_suburb_data
    - missing ≥ 5 KPI → Disregard（Print Notice）
    - missing < 5 KPI → use SA4 median for imputation
    """
    query = f"""
        SELECT
            sa2_code,
            sa2_name,
            state,
            sa4_code,
            {", ".join(KPI_COLS)}
        FROM `demografy.prod_tables.a_master_view`
    """
    df = client.query(query).to_dataframe()
    total_rows = len(df)

    # 1. count missing KPI values for each row
    missing_counts = df[KPI_COLS].isnull().sum(axis=1)

    # 2. rule 1：missing value ≥ 5 → disregard
    insufficient_mask = missing_counts >= 5
    df_insufficient = df[insufficient_mask].copy()
    df_valid = df[~insufficient_mask].copy()

    print(f"✅ data loaded (test version)")
    print(f"   Total rows: {total_rows}")
    print(f"   Valid rows: {len(df_valid)}")
    print(f"   ❌ Insufficient data rows (missing ≥ 5): {len(df_insufficient)}")

    # 3. rule 2：use SA4 median for imputation of missing < 5 KPI values
    sa4_medians = df_valid.groupby("sa4_code")[KPI_COLS].median()
    
    for sa4_code in df_valid["sa4_code"].unique():
        mask = df_valid["sa4_code"] == sa4_code
        if sa4_code in sa4_medians.index:
            df_valid.loc[mask, KPI_COLS] = df_valid.loc[mask, KPI_COLS].fillna(sa4_medians.loc[sa4_code])

    # 4. fallback: if a SA4 has no median, use the global median
    df_valid[KPI_COLS] = df_valid[KPI_COLS].fillna(df_valid[KPI_COLS].median())

    # 5. standardization
    scaler = StandardScaler()
    X = scaler.fit_transform(df_valid[KPI_COLS])

    # remove sa4_code（for similarity calculation）
    df_valid = df_valid.drop(columns=["sa4_code"])

    return df_valid, X, scaler, df_insufficient