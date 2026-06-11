import streamlit as st

from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.similarity import find_similar_suburbs

st.set_page_config(
    page_title="Demografy Suburb Look-alike Finder",
    layout="wide"
)

st.title("Suburb Look-alike Finder")

@st.cache_resource
def load_engine():
    client = get_bigquery_client()
    df, X, scaler = load_suburb_data(client)
    return df, X, scaler

df, X, scaler = load_engine()

df["display_name"] = df["sa2_name"] + " (" + df["state"] + ")"

selected_display = st.selectbox(
    "Select reference suburb",
    df["display_name"].tolist()
)

top_n = st.slider(
    "Number of matches",
    min_value=5,
    max_value=25,
    value=10
)

reference_idx = df[df["display_name"] == selected_display].index[0]

if st.button("Find similar suburbs"):
    results = find_similar_suburbs(X, reference_idx, top_n)

    rows = []

    for rank, item in enumerate(results, start=1):
        suburb = df.iloc[item["index"]]

        rows.append({
            "Rank": rank,
            "Suburb": suburb["sa2_name"],
            "State": suburb["state"],
            "Similarity": round(item["similarity"], 4)
        })

    st.dataframe(rows, use_container_width=True)