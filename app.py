import os
import logging
import streamlit as st
import pandas as pd

from engine.sample_data import get_sample_suburbs
from similarity_weighted import explain_top_contributors, find_similar_suburbs
from ui.layout import (
    render_explanation_card,
    render_placeholder_state,
    render_radar_chart,
    render_reference_summary,
    render_results_header,
    render_results_table,
    render_sidebar_controls,
)

try:
    from db.bigquery_client import get_bigquery_client
    from engine.features import load_suburb_data
    BIGQUERY_AVAILABLE = True
except ImportError:
    BIGQUERY_AVAILABLE = False

# Suppress a known Streamlit deprecation/info message about `use_container_width`
# which originates from Streamlit internals / third-party components.
# This filter ignores log records that contain the exact deprecation text.
class _IgnoreUseContainerWidthFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()
        except Exception:
            return True
        if "Please replace `use_container_width` with `width`" in msg:
            return False
        return True

logging.getLogger().addFilter(_IgnoreUseContainerWidthFilter())

st.set_page_config(
    page_title="Demografy Suburb Look-alike Finder",
    layout="wide"
)

st.title("🏘️ Suburb Look-alike Finder")


@st.cache_resource
def load_engine():
    return _load_engine_uncached()


def _load_engine_uncached():
    """Load engine without Streamlit caching (useful for tests)."""
    if BIGQUERY_AVAILABLE and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        client = get_bigquery_client()
        df, X, _ = load_suburb_data(client)
        data_source = "BigQuery"
    else:
        df, X, _ = get_sample_suburbs()
        data_source = "Sample data"

    df["display_name"] = df["sa2_name"] + " (" + df["state"] + ")"
    return df, X, data_source


df, X, data_source = load_engine()
controls = render_sidebar_controls(df["display_name"].tolist())

st.divider()

if controls["search_clicked"]:
    selected_display = controls["selected_suburb"]
    top_n = controls["top_n"]
    weight_dict = controls["weights"]
    blend_alpha = controls["blend_alpha"]
    preset = controls["preset"]
    # Map selected reference into candidate set
    original_ref_idx = int(df[df["display_name"] == selected_display].index[0])
    filtered_df = df
    filtered_positions = list(df.index)
    filtered_X = X
    if original_ref_idx not in filtered_positions:
        st.warning("Selected reference is not in the candidate set. Adjust filters.")
        render_placeholder_state()
        st.stop()

    reference_pos = filtered_positions.index(original_ref_idx)
    reference_idx = original_ref_idx

    ranked_indices, scores = find_similar_suburbs(
        filtered_X,
        reference_pos,
        top_n=top_n,
        use_weights=True,
        weight_dict=weight_dict,
    )

    numeric_indices, _ = find_similar_suburbs(
        filtered_X,
        reference_pos,
        top_n=top_n,
        use_weights=False,
    )
    numeric_rank = {int(idx): rank + 1 for rank, idx in enumerate(numeric_indices)}

    rows = []
    for rank, (idx, score) in enumerate(zip(ranked_indices, scores), start=1):
        suburb = filtered_df.iloc[int(idx)]
        delta = numeric_rank.get(int(idx), rank) - rank
        if delta > 0:
            delta_label = f"+{delta}"
        elif delta < 0:
            delta_label = str(delta)
        else:
            delta_label = "—"

        top_kpis, _ = explain_top_contributors(filtered_X, reference_pos, int(idx), top_k=2)
        rows.append(
            {
                "Rank": rank,
                "Suburb": suburb["sa2_name"],
                "State": suburb["state"],
                "Score": score,
                "Top KPIs": ", ".join(top_kpis),
                "vs numeric": delta_label,
            }
        )

    results_df = pd.DataFrame(rows)

    render_results_header(selected_display, data_source)
    reference_row = df.iloc[reference_idx]
    render_reference_summary(
        reference_row,
        [
            "kpi_1_val",
            "kpi_2_val",
            "kpi_3_val",
            "kpi_4_val",
            "kpi_5_val",
            "kpi_6_val",
            "kpi_7_val",
            "kpi_8_val",
            "kpi_9_val",
            "kpi_10_val",
        ],
        [
            "Prosperity",
            "Diversity",
            "Migration",
            "Learning",
            "Social Housing",
            "Equity",
            "Rental",
            "Anchor",
            "Mobility",
            "Young Family",
        ],
    )
    render_results_table(results_df)

    if len(results_df) > 0:
        top_match = results_df.iloc[0]["Suburb"]
        top_similarity = float(results_df.iloc[0]["Score"])
        match_row = df[df["sa2_name"] == top_match].iloc[0]
        top_kpis = results_df.iloc[0]["Top KPIs"].split(", ")

        st.divider()
        chart_col, explain_col = st.columns([3, 2], gap="large")

        with explain_col:
            render_explanation_card(
                selected_display,
                top_match,
                top_similarity,
                preset,
                blend_alpha,
                top_kpis,
            )

        with chart_col:
            render_radar_chart(
                reference_row,
                match_row,
                [
                    "kpi_1_val",
                    "kpi_2_val",
                    "kpi_3_val",
                    "kpi_4_val",
                    "kpi_5_val",
                    "kpi_6_val",
                    "kpi_7_val",
                    "kpi_8_val",
                    "kpi_9_val",
                    "kpi_10_val",
                ],
                [
                    "Prosperity",
                    "Diversity",
                    "Migration",
                    "Learning",
                    "Social Housing",
                    "Equity",
                    "Rental",
                    "Anchor",
                    "Mobility",
                    "Young Family",
                ],
            )
    else:
        render_placeholder_state()