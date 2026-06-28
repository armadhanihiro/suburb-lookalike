from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data, KPI_COLS
from engine.explain import KPI_LABELS

from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min, silhouette_score


N_REFERENCES = 10
RANDOM_STATE = 42


def make_key(row):
    return f"{row['sa2_name']} - {row['state']}"


def print_kpi_profile(row, prefix=""):
    for col in KPI_COLS:
        label = KPI_LABELS.get(col, col)
        print(f"{prefix}{label:<24}: {float(row[col]):.2f}")


def main():
    client = get_bigquery_client()

    df, x_numeric, _ = load_suburb_data(client)

    kmeans = KMeans(
        n_clusters=N_REFERENCES,
        random_state=RANDOM_STATE,
        n_init=10,
    )

    cluster_labels = kmeans.fit_predict(x_numeric)

    closest_indices, distances = pairwise_distances_argmin_min(
        kmeans.cluster_centers_,
        x_numeric,
    )

    score = silhouette_score(
        x_numeric,
        cluster_labels,
    )

    print("=== KPI-Based Reference Selection ===")
    print(f"Number of clusters: {N_REFERENCES}")
    print(f"Silhouette score: {score:.4f}")
    print("")

    for cluster_id, idx in enumerate(closest_indices):
        cluster_mask = cluster_labels == cluster_id
        cluster_size = int(cluster_mask.sum())

        representative = df.iloc[idx]
        cluster_df = df.loc[cluster_mask]

        print("=" * 70)
        print(f"Cluster {cluster_id}")
        print(f"Size: {cluster_size} suburbs")
        print(f"Representative: {make_key(representative)}")
        print(f"Distance to centroid: {distances[cluster_id]:.4f}")
        print("")

        print("Representative KPI profile:")
        print_kpi_profile(representative, prefix="  ")

        print("")
        print("Cluster average KPI profile:")

        cluster_avg = cluster_df[KPI_COLS].mean()

        for col in KPI_COLS:
            label = KPI_LABELS.get(col, col)
            print(f"  {label:<24}: {float(cluster_avg[col]):.2f}")

        print("")


if __name__ == "__main__":
    main()