import numpy as np

KPI_LABELS = {
    "kpi_1_val": "Prosperity",
    "kpi_2_val": "Diversity",
    "kpi_3_val": "Migration Footprint",
    "kpi_4_val": "Learning Level",
    "kpi_5_val": "Social Housing",
    "kpi_6_val": "Resident Equity",
    "kpi_7_val": "Rental Access",
    "kpi_8_val": "Resident Anchor",
    "kpi_9_val": "Household Mobility",
    "kpi_10_val": "Young Family",
}

def get_top_contributing_kpis(X_numeric, reference_idx, match_idx, kpi_cols, top_n=3):
    reference_vector = X_numeric[reference_idx]
    match_vector = X_numeric[match_idx]

    differences = np.abs(reference_vector - match_vector)
    top_indices = np.argsort(differences)[:top_n]

    return [
        KPI_LABELS.get(kpi_cols[i], kpi_cols[i]) 
        for i in top_indices
    ]

def build_rank_map(results):
    return {
        item["index"]: rank
        for rank, item in enumerate(results, start=1)
    }


def get_rank_delta(match_idx, numeric_results, hybrid_rank,):
    numeric_rank_map = build_rank_map(numeric_results)
    numeric_rank = numeric_rank_map.get(match_idx)

    if numeric_rank is None:
        return "New"

    delta = numeric_rank - hybrid_rank
    if delta > 0:
        return f"+{delta}"

    if delta < 0:
        return str(delta)

    return "0"


def get_radar_data(df, reference_idx, match_idx, kpi_cols,):
    reference_row = df.iloc[reference_idx]
    match_row = df.iloc[match_idx]

    return {
        "labels": [
            KPI_LABELS.get(col, col)
            for col in kpi_cols
        ],
        "reference_values": [
            reference_row[col]
            for col in kpi_cols
        ],
        "match_values": [
            match_row[col]
            for col in kpi_cols
        ],
    }