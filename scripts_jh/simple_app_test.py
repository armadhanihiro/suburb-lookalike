import streamlit as st
from google.cloud import bigquery
from engine.features import load_suburb_data

# 定义州名缩写映射
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

@st.cache_data
def load_data():
    client = bigquery.Client.from_service_account_json(
        r"E:\DAX\AI\Project AI\suburb-similarity\suburb-similarity-team\secrets\demografy-bigquery.json"
    )
    df, X, scaler = load_suburb_data(client)
    
    # 在这里加映射，只做一次
    df["state_display"] = df["state"].map(STATE_ABBR).fillna(df["state"])
    df["display_name"] = df["sa2_name"] + " (" + df["state_display"] + ")"
    
    return df, X, scaler

df, X, scaler = load_data()

st.title("🏘️ Suburb Look‑alike Finder")
st.write(f"✅ data loaded successfully {len(df)} suburbs")
st.dataframe(df[["display_name"]].head())