"""Layout and UI component helpers for the Streamlit app."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_sidebar_controls(display_names, kpi_cols, kpi_labels, access):
    with st.sidebar:
        st.image("assets/demografy-logo.png", width=180)

        st.markdown("### 🏡 Controls")

        with st.container(border=True):
            st.markdown(f"**{access['user_id']} · {access['tier']}**")
            remaining = access["lookup_limit"] - access["lookups_used"]
            st.caption(f"{remaining} / {access['lookup_limit']} lookups left")
            st.caption(f"Match cap: {access['match_cap']}")

        selected_suburb = st.selectbox("Reference suburb", display_names)

        match_cap = access["match_cap"]
        top_n = st.slider(
            "Matches to return",
            min_value=1,
            max_value=match_cap,
            value=min(10, match_cap),
        )

        st.divider()

        st.markdown("### ⚙️ KPI weights")
        st.caption("Scale KPI importance in the similarity score.")

        if "preset" not in st.session_state:
            st.session_state.preset = "Custom"

        preset_cols = st.columns(3)

        with preset_cols[0]:
            if st.button("Investor", use_container_width=True):
                st.session_state.preset = "Investor"

        with preset_cols[1]:
            if st.button("Family", use_container_width=True):
                st.session_state.preset = "Family"

        with preset_cols[2]:
            if st.button("Lifestyle", use_container_width=True):
                st.session_state.preset = "Lifestyle"

        preset = st.session_state.preset
        st.caption(f"Current preset: **{preset}**")

        preset_weights = {
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

        visible_cols = ["kpi_1_val", "kpi_2_val", "kpi_10_val"]
        weights = {}

        for col in visible_cols:
            label = kpi_labels[kpi_cols.index(col)]
            default_value = preset_weights.get(preset, {}).get(col, 1.0)

            weights[col] = st.slider(
                label,
                min_value=0.0,
                max_value=2.0,
                value=float(default_value),
                step=0.1,
            )

        with st.expander("+7 more KPI sliders"):
            for col in kpi_cols:
                if col in visible_cols:
                    continue

                label = kpi_labels[kpi_cols.index(col)]
                default_value = preset_weights.get(preset, {}).get(col, 1.0)

                weights[col] = st.slider(
                    label,
                    min_value=0.0,
                    max_value=2.0,
                    value=float(default_value),
                    step=0.1,
                )

        st.divider()

        blend_alpha = st.slider(
            "Blend α",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.1,
            help="0 = numeric KPI only, 1 = text embedding only",
        )

        st.caption("numeric ←→ text")

        search_clicked = st.button(
            "🔍 Find similar suburbs",
            use_container_width=True,
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
    st.header(f"📊 Suburbs most like {reference_suburb}")

    if data_source:
        st.caption(f"Data source: {data_source}")


def render_reference_summary(reference_row: pd.Series, kpi_cols: list[str], kpi_labels: list[str]):
    st.subheader("🏡 Reference suburb profile")

    suburb_display = f"{reference_row['sa2_name']} ({reference_row['state']})"

    kpi_values = [float(reference_row[col]) for col in kpi_cols]
    kpi_data = list(zip(kpi_labels, kpi_values))
    top_kpis = sorted(kpi_data, key=lambda item: item[1], reverse=True)[:3]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f"**{suburb_display}** is the selected reference suburb.")
        st.markdown("**Top KPI strengths**")

        for label, value in top_kpis:
            st.markdown(f"- **{label}**: {value:.1f}")

    with col2:
        for label, value in top_kpis:
            st.metric(label, f"{value:.1f}")


def render_results_table(results_df: pd.DataFrame):
    st.subheader("Top matches")

    display_df = results_df.copy()
    display_df["Score"] = display_df["Score"].map(lambda x: f"{x:.2f}")

    st.dataframe(
        display_df.drop(columns=["_match_idx"], errors="ignore"),
        use_container_width=True,
        hide_index=True,
    )


def render_explanation_card(
    reference_suburb: str,
    top_match: str,
    similarity_score: float,
    preset: str,
    blend_alpha: float,
    top_kpis: list[str],
):
    st.subheader("📝 Why these match")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(
            f"**{top_match}** is similar to **{reference_suburb}** under the current settings. "
            f"The selected preset is **{preset}**, and the blend is set to **{blend_alpha:.1f}**."
        )

        if top_kpis:
            st.markdown("### Top drivers")
            for kpi in top_kpis[:3]:
                st.markdown(f"- **{kpi}**")

    with col2:
        st.metric("Similarity score", f"{similarity_score:.1f}")
        st.caption("/100")
        st.metric("Blend α", f"{blend_alpha:.1f}")

    st.markdown(
        "This match is driven by close KPI patterns and the semantic suburb profile embedding."
    )


def render_radar_chart(reference_row: pd.Series, match_row: pd.Series, kpi_cols: list[str], kpi_labels: list[str]):
    st.subheader("📈 KPI comparison")

    reference_values = [float(reference_row[col]) for col in kpi_cols]
    match_values = [float(match_row[col]) for col in kpi_cols]

    categories = kpi_labels + [kpi_labels[0]]
    reference_trace = reference_values + [reference_values[0]]
    match_trace = match_values + [match_values[0]]

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=reference_trace,
                theta=categories,
                fill="toself",
                name="Reference suburb",
                line=dict(color="#5e17eb"),
            ),
            go.Scatterpolar(
                r=match_trace,
                theta=categories,
                fill="toself",
                name="Selected matching suburb",
                line=dict(color="#8df2ed"),
            ),
        ]
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(reference_values), max(match_values)) * 1.1],
            )
        ),
        showlegend=True,
        margin=dict(l=20, r=20, t=20, b=20),
        height=500,
    )

    st.plotly_chart(fig, use_container_width=True)


def render_placeholder_state():
    st.warning("⏳ Use the sidebar to choose a suburb and run the similarity search.")

    st.markdown(
        """
        ### Suburb look-alike finder

        Use the left panel to select a suburb, tune KPI importance, adjust the blend value, and run a search.
        """
    )