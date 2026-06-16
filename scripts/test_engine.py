from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.similarity import find_similar_suburbs

client = get_bigquery_client()
df, X, scaler = load_suburb_data(client)

print("Total suburbs:", len(df))
print("Feature matrix shape:", X.shape)

reference_idx = 0
results = find_similar_suburbs(X, reference_idx, top_n=10)

print("\nReference:")
print(df.iloc[reference_idx][["sa2_code", "sa2_name", "state"]])

print("\nTop matches:")
for rank, result in enumerate(results, start=1):
    suburb = df.iloc[result["index"]]
    print(
        rank,
        suburb["sa2_name"],
        suburb["state"],
        round(result["similarity"], 4)
    )