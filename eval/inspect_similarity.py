from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data, KPI_COLS
from engine.text_embed import load_or_create_embeddings
from engine.fusion import fuse_vectors
from engine.similarity import find_similar_suburbs
import sys

from engine.explain import KPI_LABELS

REFERENCE = sys.argv[1] if len(sys.argv) > 1 else "Googong"
ALPHA = 0.4


def print_profile(row):
    print(f"\n{row['sa2_name']} - {row['state']}")

    for col in KPI_COLS:
        label = KPI_LABELS.get(col, col)
        print(f"  {label}: {row[col]:.2f}")

def print_kpi_difference(reference, candidate):
    print("-" * 60)

    total_diff = 0

    for col in KPI_COLS:
        label = KPI_LABELS.get(col, col)

        ref = float(reference[col])
        cand = float(candidate[col])

        diff = cand - ref
        total_diff += abs(diff)

        print(
            f"{label:<22}"
            f"{ref:>7.2f}"
            f" -> "
            f"{cand:>7.2f}"
            f" ({diff:+6.2f})"
        )

    avg_diff = total_diff / len(KPI_COLS)

    print("-" * 60)
    print(f"Average KPI Difference : {avg_diff:.2f}")


def main():
    client = get_bigquery_client()

    df, x_numeric, _ = load_suburb_data(client)

    x_text = load_or_create_embeddings(
        profiles=[],
        cache_path="cache/suburb_embeddings.npy",
    )

    x_hybrid = fuse_vectors(
        x_numeric,
        x_text,
        alpha=ALPHA,
    )

    reference_idx = df[df["sa2_name"] == REFERENCE].index[0]

    print("=" * 60)
    print("REFERENCE")
    print("=" * 60)

    print_profile(df.iloc[reference_idx])

    print("\n")
    print("=" * 60)
    print("TOP MATCHES")
    print("=" * 60)

    results = find_similar_suburbs(
        x_hybrid,
        reference_idx,
        top_n=10,
    )

    for rank, item in enumerate(results, start=1):
        row = df.iloc[item["index"]]

        print(f"\n#{rank}  Similarity : {item['similarity']:.4f}")
        print(f"{row['sa2_name']} - {row['state']}")

        print_kpi_difference(
            df.iloc[reference_idx],
            row,
        )
if __name__ == "__main__":
    main()