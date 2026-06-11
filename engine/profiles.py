from engine.features import KPI_COLS

KPI_NAMES = {
    "kpi_1_val": "prosperity",
    "kpi_2_val": "cultural diversity",
    "kpi_3_val": "migration footprint",
    "kpi_4_val": "learning level",
    "kpi_5_val": "social housing presence",
    "kpi_6_val": "resident equity",
    "kpi_7_val": "rental affordability",
    "kpi_8_val": "resident stability",
    "kpi_9_val": "household mobility potential",
    "kpi_10_val": "young family presence",
}


def describe_level(value, series):
    low_threshold = series.quantile(0.33)
    high_threshold = series.quantile(0.66)

    if value >= high_threshold:
        return "high"
    elif value <= low_threshold:
        return "low"

    return "moderate"


def generate_suburb_profile(row, df):
    suburb = row["sa2_name"]
    state = row["state"]

    prosperity = describe_level(
        row["kpi_1_val"],
        df["kpi_1_val"]
    )

    diversity = describe_level(
        row["kpi_2_val"],
        df["kpi_2_val"]
    )

    migration = describe_level(
        row["kpi_3_val"],
        df["kpi_3_val"]
    )

    learning = describe_level(
        row["kpi_4_val"],
        df["kpi_4_val"]
    )

    rental = describe_level(
        row["kpi_7_val"],
        df["kpi_7_val"]
    )

    family = describe_level(
        row["kpi_10_val"],
        df["kpi_10_val"]
    )

    return (
        f"{suburb}, {state} has "
        f"{prosperity} prosperity, "
        f"{diversity} cultural diversity, "
        f"{migration} migration footprint, "
        f"{learning} education profile, "
        f"{rental} rental characteristics, "
        f"and {family} young family presence."
    )


def generate_profiles(df):
    return df.apply(
        lambda row: generate_suburb_profile(row, df),
        axis=1
    ).tolist()