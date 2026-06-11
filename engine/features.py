import pandas as pd
from sklearn.preprocessing import StandardScaler

KPI_COLS = [f"kpi_{i}_val" for i in range(1, 11)]

def load_suburb_data(client):
    query = f"""
        SELECT
            sa2_code,
            sa2_name,
            state,
            {", ".join(KPI_COLS)}
        FROM `demografy.prod_tables.a_master_view`
    """

    df = client.query(query).to_dataframe()

    df[KPI_COLS] = df[KPI_COLS].fillna(df[KPI_COLS].median())

    # Standardise KPI values
    scaler = StandardScaler()
    X = scaler.fit_transform(df[KPI_COLS])

    return df, X, scaler