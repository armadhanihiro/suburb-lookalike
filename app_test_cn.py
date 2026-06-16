import streamlit as st
from google.cloud import bigquery
from engine.features import load_suburb_data   # 你的特征加载函数
from similarity_weighted import find_similar_suburbs   # 你刚更新的相似度函数

# ---------- 1. 连接 BigQuery 并加载数据 ----------
@st.cache_data
def load_data():
    client = bigquery.Client.from_service_account_json(
        r"E:\DAX\AI\Project AI\suburb-similarity\suburb-similarity-team\secrets\demografy-bigquery.json"
    )
    df, X, scaler = load_suburb_data(client)
    return df, X

df, X = load_data()

# ---------- 2. Streamlit 界面 ----------
st.title("Suburb Look-alike Finder")
st.caption("基于 Demografy KPI 的相似郊区推荐（有权重 + 0–100 分）")

suburb_names = df["sa2_name"].tolist()
selected_name = st.selectbox("选择一个郊区", suburb_names)

if st.button("🔍 查找相似郊区"):
    idx = df[df["sa2_name"] == selected_name].index[0]
    top_idx, scores = find_similar_suburbs(X, idx, top_n=10, use_weights=True)

    st.subheader("🏘️ Top 10 相似郊区")
    for rank, (i, score) in enumerate(zip(top_idx, scores), start=1):
        name = df.loc[i, "sa2_name"]
        st.write(f"{rank}. **{name}** — 相似度: {score:.1f} / 100")