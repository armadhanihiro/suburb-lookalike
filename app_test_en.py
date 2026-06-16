import streamlit as st
from google.cloud import bigquery
from engine.features import load_suburb_data
from similarity_weighted import find_similar_suburbs

# ============================================================
# 1. State abbreviation mapping
# ============================================================
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
    "Outside Australia": "OA"
}

# ============================================================
# 2. Load data (cached)
# ============================================================
@st.cache_data
def load_data():
    client = bigquery.Client.from_service_account_json(
        r"E:\DAX\AI\Project AI\suburb-similarity\suburb-similarity-team\secrets\demografy-bigquery.json"
    )
    df, X, scaler = load_suburb_data(client)
    
    # Add display fields
    df["state_abbr"] = df["state"].map(STATE_ABBR).fillna(df["state"])
    df["display_name"] = df["sa2_name"] + " (" + df["state_abbr"] + ")"
    
    return df, X

# Load data once at startup
df, X = load_data()

# ============================================================
# 3. Streamlit UI
# ============================================================
st.set_page_config(page_title="Suburb Similarity Finder", layout="wide")
st.title("🏘️ Suburb Look‑alike Finder")
st.caption("Powered by Demografy KPI + weighted cosine similarity (0–100 score)")

# Dropdown using display_name
suburb_list = df["display_name"].tolist()
selected_display = st.selectbox("Select a suburb", suburb_list)

if st.button("🔍 Find Similar Suburbs"):
    # Get original index
    idx = df[df["display_name"] == selected_display].index[0]
    
    # Find top 10 similar suburbs
    top_idx, scores = find_similar_suburbs(X, idx, top_n=10, use_weights=True)
    
    st.subheader("🏘️ Top 10 Most Similar Suburbs")
    for rank, (i, score) in enumerate(zip(top_idx, scores), start=1):
        name = df.loc[i, "display_name"]
        st.write(f"{rank}. **{name}** — Similarity: {score:.1f} / 100")