import logging
import os

import numpy as np
import pandas as pd
import streamlit as st

from engine.logging_utils import now_ms, elapsed_ms, log_search

from engine.explain import KPI_LABELS, get_rank_delta, get_top_contributing_kpis
from engine.features import KPI_COLS
from engine.fusion import fuse_vectors
from engine.sample_data import get_sample_suburbs
from engine.similarity import find_similar_suburbs
from engine.text_embed import load_or_create_embeddings
from engine.index import build_faiss_index, search_index
from engine.rbac import (
    cap_top_n,
    increment_lookup,
    has_lookup_remaining,
)
from engine.user_login import login_screen

# Removed interactive login UI: use a default local access when not provided

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


class _IgnoreUseContainerWidthFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()
        except Exception:
            return True

        return "Please replace `use_container_width` with `width`" not in msg


logging.getLogger().addFilter(_IgnoreUseContainerWidthFilter())


st.set_page_config(
    page_title="Demografy Suburb Look-alike Finder",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sauce+Sans:wght@400;500;600;700&display=swap&text=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789');

    html, body, .stApp, .main, .block-container, .element-container, .css-1cpxqw2, .css-1d391kg {
        font-family: 'Open Sauce Sans', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6, .stText, .stMarkdown {
        font-family: 'Open Sauce Sans', sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_engine():
    if BIGQUERY_AVAILABLE:
        try:
            client = get_bigquery_client()
            df, x_numeric, _ = load_suburb_data(client)

            x_text = load_or_create_embeddings(
                profiles=[],
                cache_path="cache/suburb_embeddings.npy",
            )

            data_source = "BigQuery"

        except Exception as error:
            st.warning(
                f"BigQuery could not be loaded. "
                f"Using sample data instead. Error: {error}"
            )

            df, x_numeric, _ = get_sample_suburbs()
            x_text = None
            data_source = "Sample data"

    else:
        df, x_numeric, _ = get_sample_suburbs()
        x_text = None
        data_source = "Sample data"

    STATE_ABBR = {
        "New South Wales": "NSW",
        "Victoria": "VIC",
        "Queensland": "QLD",
        "Western Australia": "WA",
        "South Australia": "SA",
        "Tasmania": "TAS",
        "Australian Capital Territory": "ACT",
        "Northern Territory": "NT",
        "Other Territories": "OT",
        "Outside Australia": "OA",
    }

    df["state_abbr"] = df["state"].map(STATE_ABBR).fillna(df["state"])
    df["display_name"] = (
        df["sa2_name"] + " (" + df["state_abbr"] + ")"
    )

    return df, x_numeric, x_text, data_source


def apply_kpi_weights(x_numeric, weights):
    weight_vector = np.array(
        [weights.get(col, 1.0) for col in KPI_COLS],
        dtype="float32",
    )

    return x_numeric * weight_vector


KPI_DISPLAY_LABELS = [
    KPI_LABELS.get(col, col)
    for col in KPI_COLS
]

def main():
    if "access" not in st.session_state:
        st.session_state.access = None

    if st.session_state.access is None:

        user_access = login_screen()

        if user_access:
            st.session_state.access = user_access
            st.rerun()

        st.stop()

    access = st.session_state.access

    with st.sidebar:
        st.image("assets/demografy-logo.png", width=180)

        st.write(
            f"👋 Welcome, **{access.get('user_id', 'User')}**"
        )

        if st.button(
            "Logout",
            use_container_width=True,
            key="logout_button",
        ):
            st.session_state.access = None
            st.cache_data.clear()
            st.rerun()

    df, x_numeric, x_text, data_source = load_engine()

    controls = render_sidebar_controls(
        df["display_name"].tolist(),
        KPI_COLS,
        KPI_DISPLAY_LABELS,
        access,
    )

    st.title("Suburb Look-alike Finder")
    st.divider()


    if controls["search_clicked"]:
        start_time = now_ms()
        if not access["is_active"]:
            st.error("User account is inactive.")
            st.stop()

        if not has_lookup_remaining(access):
            st.error("You have reached your lookup limit.")
            st.stop()

        st.session_state.access = increment_lookup(access)
        access = st.session_state.access

        selected_display = controls["selected_suburb"]
        top_n = controls["top_n"]
        top_n = cap_top_n(top_n, access)
        weights = controls["weights"]
        blend_alpha = controls["blend_alpha"]
        preset = controls["preset"]

        reference_idx = int(
            df[df["display_name"] == selected_display].index[0]
        )

        if x_text is None:
            st.warning(
                "Gemini embedding cache is not available. Please run "
                "`python -m scripts.build_embeddings` first."
            )
            st.stop()

        weighted_x_numeric = apply_kpi_weights(
            x_numeric,
            weights,
        )

        x_hybrid = fuse_vectors(
            weighted_x_numeric,
            x_text,
            alpha=blend_alpha,
        )

        faiss_index = build_faiss_index(x_hybrid)

        scores, indices = search_index(
            faiss_index,
            x_hybrid[reference_idx].reshape(1, -1),
            top_n=top_n + 1,
        )

        hybrid_results = []

        for score, idx in zip(scores, indices):
            if idx == reference_idx:
                continue

            hybrid_results.append(
                {
                    "index": int(idx),
                    "similarity": float(score),
                }
            )

            if len(hybrid_results) == top_n:
                break

        numeric_results = find_similar_suburbs(
            weighted_x_numeric,
            reference_idx,
            top_n=100,
        )

        rows = []

        for rank, item in enumerate(hybrid_results, start=1):
            match_idx = int(item["index"])
            suburb = df.iloc[match_idx]

            top_kpis = get_top_contributing_kpis(
                weighted_x_numeric,
                reference_idx,
                match_idx,
                KPI_COLS,
                top_n=3,
            )

            rank_delta = get_rank_delta(
                match_idx,
                numeric_results,
                rank,
            )

            rows.append(
                {
                    "Rank": rank,
                    "Suburb": suburb["sa2_name"],
                    "State": suburb["state_abbr"],
                    "Score": round(float(item["similarity"]) * 100, 2),
                    "Top KPIs": ", ".join(top_kpis),
                    "vs numeric": rank_delta,
                    "_match_idx": match_idx,
                }
            )

        results_df = pd.DataFrame(rows)

        log_search(
            user_id=access["user_id"],
            reference=selected_display,
            alpha=blend_alpha,
            top_n=top_n,
            preset=preset,
            data_source=data_source,
            duration_ms=elapsed_ms(start_time),
            results=[
                {
                    "rank": row["Rank"],
                    "suburb": row["Suburb"],
                    "state": row["State"],
                    "score": row["Score"],
                    "top_kpis": row["Top KPIs"],
                    "vs_numeric": row["vs numeric"],
                } for row in rows
            ],
        )

        st.session_state.results_df = results_df
        st.session_state.reference_idx = reference_idx
        st.session_state.selected_display = selected_display
        st.session_state.preset = preset
        st.session_state.blend_alpha = blend_alpha


    if "results_df" in st.session_state:
        results_df = st.session_state.results_df
        reference_idx = st.session_state.reference_idx
        selected_display = st.session_state.selected_display
        preset = st.session_state.preset
        blend_alpha = st.session_state.blend_alpha

        render_results_header(
            selected_display,
            data_source,
        )

        reference_row = df.iloc[reference_idx]

        render_reference_summary(
            reference_row,
            KPI_COLS,
            KPI_DISPLAY_LABELS,
        )

        render_results_table(results_df)

        selected_row_pos = st.selectbox(
            "Choose match to explain",
            options=list(range(len(results_df))),
            format_func=lambda i: (
                f"{results_df.iloc[i]['Rank']}. "
                f"{results_df.iloc[i]['Suburb']} "
                f"({results_df.iloc[i]['State']})"
            ),
        )

        selected_result = results_df.iloc[selected_row_pos]

        match_idx = int(selected_result["_match_idx"])
        match_row = df.iloc[match_idx]

        match_name = match_row["sa2_name"]
        match_similarity = float(selected_result["Score"])
        top_kpis = selected_result["Top KPIs"].split(", ")

        st.divider()

        chart_col, explain_col = st.columns([3, 2], gap="large")

        with explain_col:
            render_explanation_card(
                selected_display,
                match_name,
                match_similarity,
                preset,
                blend_alpha,
                top_kpis,
            )

        with chart_col:
            render_radar_chart(
                reference_row,
                match_row,
                KPI_COLS,
                KPI_DISPLAY_LABELS,
            )

    else:
        render_placeholder_state()

if __name__ == "__main__":
    main()