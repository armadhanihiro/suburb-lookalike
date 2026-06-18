"""Layout and UI component helpers for the Streamlit app."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

KPI_SLIDER_CONFIG = [
    ("Prosperity", "kpi_1_val", 1.0),
    ("Diversity", "kpi_2_val", 1.0),
    ("Young family", "kpi_10_val", 1.0),
]

ALL_KPI_KEYS = [
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
]

KPI_LABELS = [
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
]

PRESET_WEIGHTS = {
    "Investor": {
        "kpi_1_val": 1.6,
        "kpi_2_val": 0.8,
        "kpi_10_val": 1.2,
    },
    "Family": {
        "kpi_1_val": 1.0,
        "kpi_2_val": 1.2,
        "kpi_10_val": 1.8,
    },
    "Lifestyle": {
        "kpi_1_val": 0.9,
        "kpi_2_val": 1.5,
        "kpi_10_val": 1.3,
    },
}


def get_preset_weights(preset: str) -> dict[str, float]:
    """Return base weights for the visible KPI sliders for a given preset."""
    preset_values = PRESET_WEIGHTS.get(preset, {})
    return {
        key: preset_values.get(key, default)
        for _, key, default in KPI_SLIDER_CONFIG
    }


def render_sidebar_controls(suburbs_list: list):
    """
    Render sidebar control panel with reference suburb selection and match settings.
    
    Args:
        suburbs_list: List of suburb display names
    
    Returns:
        dict: Contains selected_suburb, top_n and other control settings
    """
    st.sidebar.header("🏘️ Controls")

    selected_suburb = st.sidebar.selectbox(
        "Reference suburb",
        suburbs_list,
        help="Choose a suburb to find similar matches for",
    )

    top_n = st.sidebar.slider(
        "Matches to return",
        min_value=5,
        max_value=25,
        value=10,
        help="How many similar suburbs to display",
    )

    st.sidebar.divider()
    st.sidebar.subheader("⚙️ KPI weights")
    st.sidebar.caption("Scale the importance of each KPI in the similarity score.")

    if "preset" not in st.session_state:
        st.session_state["preset"] = "Custom"
    preset = st.session_state["preset"]

    st.sidebar.divider()
    st.sidebar.subheader("🎯 Presets")

    preset_cols = st.sidebar.columns(3)
    if preset_cols[0].button("Investor"):
        st.session_state["preset"] = "Investor"
        for _, key, _ in KPI_SLIDER_CONFIG:
            st.session_state[f"weight_{key}"] = PRESET_WEIGHTS["Investor"].get(key, 1.0)
    if preset_cols[1].button("Family"):
        st.session_state["preset"] = "Family"
        for _, key, _ in KPI_SLIDER_CONFIG:
            st.session_state[f"weight_{key}"] = PRESET_WEIGHTS["Family"].get(key, 1.0)
    if preset_cols[2].button("Lifestyle"):
        st.session_state["preset"] = "Lifestyle"
        for _, key, _ in KPI_SLIDER_CONFIG:
            st.session_state[f"weight_{key}"] = PRESET_WEIGHTS["Lifestyle"].get(key, 1.0)

    preset = st.session_state["preset"]
    st.sidebar.caption(f"Current preset: **{preset}**")

    weights = {key: 1.0 for key in ALL_KPI_KEYS}
    for label, key, default in KPI_SLIDER_CONFIG:
        slider_key = f"weight_{key}"
        if slider_key not in st.session_state:
            st.session_state[slider_key] = default

        weights[key] = st.sidebar.slider(
            label,
            min_value=0.0,
            max_value=2.0,
            value=st.session_state[slider_key],
            step=0.1,
            key=slider_key,
            help=f"Adjust weight for {label}",
        )

    if preset != "Custom":
        preset_values = PRESET_WEIGHTS.get(preset, {})
        for _, key, default in KPI_SLIDER_CONFIG:
            slider_key = f"weight_{key}"
            if st.session_state[slider_key] != preset_values.get(key, default):
                st.session_state["preset"] = "Custom"
                preset = "Custom"
                break

    st.sidebar.divider()
    blend_alpha = st.sidebar.slider(
        "Blend (α)",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.1,
        help="Blend numeric similarity (0) and text-style diversity (1)",
    )

    search_clicked = st.sidebar.button(
        "🔍 Find similar suburbs",
        width="stretch",
    )

    return {
        "selected_suburb": selected_suburb,
        "top_n": top_n,
        "weights": weights,
        "blend_alpha": blend_alpha,
        "preset": preset,
        "search_clicked": search_clicked,
    }


def render_results_header(reference_suburb: str, data_source: str | None = None):
    """Render the main page header for a selected suburb."""
    st.header(f"📊 Suburbs most like {reference_suburb}")
    st.write(
        "Use the sidebar controls to tune KPI weights, select presets, and compare the most similar suburbs."
    )


def render_reference_summary(reference_row: pd.Series, kpi_cols: list[str], kpi_labels: list[str]):
    """Render a compact profile summary for the reference suburb."""
    st.subheader("🏡 Reference suburb profile")

    suburb_display = f"{reference_row['sa2_name']} ({reference_row['state']})"
    kpi_values = [float(reference_row[col]) for col in kpi_cols]
    kpi_data = list(zip(kpi_labels, kpi_values))
    top_kpis = sorted(kpi_data, key=lambda item: item[1], reverse=True)[:3]

    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{suburb_display}** is the selected reference suburb for this search.")
            st.markdown("**Top KPI strengths**")
            for label, value in top_kpis:
                st.markdown(f"- **{label}**: {value:.1f}")
        with col2:
            for label, value in top_kpis:
                st.metric(label, f"{value:.1f}")


def render_results_table(results_df: pd.DataFrame):
    """Render the majority of the ranked similarity result table."""
    st.subheader("Top matches")
    display_df = results_df.copy()
    display_df["Score"] = display_df["Score"].map(lambda x: f"{x:.2f}")
    display_df = display_df.set_index("Rank")

    st.table(display_df)


def render_explanation_card(
    reference_suburb: str,
    top_match: str,
    similarity_score: float,
    preset: str,
    blend_alpha: float,
    top_kpis: list[str],
):
    """Render an explanation card for the highest ranked match."""
    st.subheader("📝 Why these match")

    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f"**{top_match}** is the closest match to **{reference_suburb}** under the current settings. "
                f"The selected preset is **{preset}**, and the blend is set to **{blend_alpha:.1f}**."
            )
            kpi_items = top_kpis[:2]
            if kpi_items:
                st.markdown("### Top drivers")
                for kpi in kpi_items:
                    st.markdown(f"- **{kpi}**")
        with col2:
            st.metric("Similarity score", f"{similarity_score:.1f}/100")
            st.metric("Blend α", f"{blend_alpha:.1f}")

    st.markdown(
        "This match is driven by the KPIs shown above and the weight settings you chose. "
        "Adjust the sliders to see how the result ranking changes."
    )


def render_radar_chart(reference_row: pd.Series, match_row: pd.Series, kpi_cols: list[str], kpi_labels: list[str]):
    """Render a radar chart comparing the reference suburb against the top match."""
    st.subheader("📈 KPI comparison")

    reference_values = reference_row[kpi_cols].tolist()
    match_values = match_row[kpi_cols].tolist()
    categories = kpi_labels + [kpi_labels[0]]
    reference_trace = reference_values + [reference_values[0]]
    match_trace = match_values + [match_values[0]]

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=reference_trace,
                theta=categories,
                fill="toself",
                name="Reference",
                line=dict(color="#1f77b4"),
            ),
            go.Scatterpolar(
                r=match_trace,
                theta=categories,
                fill="toself",
                name="Top match",
                line=dict(color="#2ca02c"),
            ),
        ]
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(max(reference_values), max(match_values)) * 1.1])
        ),
        showlegend=True,
        margin=dict(l=20, r=20, t=20, b=20),
        height=500,
    )
    st.plotly_chart(fig, width="stretch")


def render_radar_chart_placeholder():
    """Render a placeholder for dashboard KPI comparison."""
    st.subheader("📈 KPI comparison")
    st.info("Radar chart and KPI comparison will be added in Phase 2.")


def render_placeholder_state():
    """Render the placeholder state before the first search."""
    st.warning("⏳ Use the sidebar to choose a suburb and run the similarity search.")

    with st.container():
        st.markdown(
            """
            ### Suburb look-alike finder

            The UI is ready for Phase 1.
            Use the left panel to select a suburb, tune KPI importance, and run a search.

            Phase 2 will add:
            - a visual KPI radar comparison,
            - real dataset integration,
            - richer explanation text,
            - additional filters.
            """
        )
