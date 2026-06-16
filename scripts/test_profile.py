from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.profiles import generate_profiles

client = get_bigquery_client()
df, X, scaler = load_suburb_data(client)

profiles = generate_profiles(df)

print("Total profiles:", len(profiles))
print("\nSample profiles:")
for profile in profiles[:5]:
    print("-", profile)