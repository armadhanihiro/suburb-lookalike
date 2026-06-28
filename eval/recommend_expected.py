import sys

from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data, KPI_COLS
from engine.text_embed import load_or_create_embeddings
from engine.fusion import fuse_vectors
from engine.similarity import find_similar_suburbs


DEFAULT_REFERENCE = "Birkdale"
ALPHA = 0.4
TOP_N_CANDIDATES = 15
TOP_N_EXPECTED = 5
CACHE_PATH = "cache/suburb_embeddings.npy"

HYBRID_WEIGHT = 0.7
KPI_WEIGHT = 0.3


def make_key(row):
    return f"{row['sa2_name']} - {row['state']}"


def average_kpi_difference(reference_row, candidate_row):
    total_diff = 0.0

    for col in KPI_COLS:
        total_diff += abs(
            float(candidate_row[col]) - float(reference_row[col])
        )

    return total_diff / len(KPI_COLS)


def normalize_kpi_similarity(avg_diff, max_diff):
    if max_diff == 0:
        return 1.0

    return 1 - (avg_diff / max_diff)


def main():
    reference_name = (
        sys.argv[1]
        if len(sys.argv) > 1
        else DEFAULT_REFERENCE
    )

    client = get_bigquery_client()
    df, x_numeric, _ = load_suburb_data(client)

    reference_rows = df[df["sa2_name"] == reference_name]

    if reference_rows.empty:
        print(f"Reference not found: {reference_name}")
        return

    reference_idx = int(reference_rows.index[0])
    reference_row = df.iloc[reference_idx]

    x_text = load_or_create_embeddings(
        profiles=[],
        cache_path=CACHE_PATH,
    )

    x_hybrid = fuse_vectors(
        x_numeric,
        x_text,
        alpha=ALPHA,
    )

    results = find_similar_suburbs(
        x_hybrid,
        reference_idx,
        top_n=TOP_N_CANDIDATES,
    )

    candidates = []

    for item in results:
        candidate_row = df.iloc[item["index"]]

        avg_diff = average_kpi_difference(
            reference_row,
            candidate_row,
        )

        candidates.append(
            {
                "key": make_key(candidate_row),
                "hybrid_similarity": float(item["similarity"]),
                "avg_kpi_diff": avg_diff,
            }
        )

    max_diff = max(
        candidate["avg_kpi_diff"]
        for candidate in candidates
    )

    for candidate in candidates:
        candidate["kpi_similarity"] = normalize_kpi_similarity(
            candidate["avg_kpi_diff"],
            max_diff,
        )

        candidate["final_score"] = (
            HYBRID_WEIGHT * candidate["hybrid_similarity"]
            + KPI_WEIGHT * candidate["kpi_similarity"]
        )

    candidates = sorted(
        candidates,
        key=lambda item: item["final_score"],
        reverse=True,
    )

    selected = candidates[:TOP_N_EXPECTED]

    print("=== Recommended Expected Neighbours ===")
    print(f"Reference: {make_key(reference_row)}")
    print(f"Alpha: {ALPHA}")
    print(
        f"Final score = {HYBRID_WEIGHT} hybrid similarity "
        f"+ {KPI_WEIGHT} KPI similarity"
    )
    print("")

    for rank, candidate in enumerate(selected, start=1):
        print(
            f"{rank}. {candidate['key']} | "
            f"hybrid={candidate['hybrid_similarity']:.4f} | "
            f"kpi_sim={candidate['kpi_similarity']:.4f} | "
            f"avg_diff={candidate['avg_kpi_diff']:.2f} | "
            f"final={candidate['final_score']:.4f}"
        )

    print("")
    print("=== Copy to golden_set.py ===")
    print("")
    print("GoldenReference(")
    print(f'    reference="{make_key(reference_row)}",')
    print("    expected=[")

    for candidate in selected:
        print(f'        "{candidate["key"]}",')

    print("    ],")
    print("    rationale=(")
    print(
        '        "Selected using combined hybrid similarity and KPI similarity. "'
    )
    print(
        '        "These neighbours were chosen because they ranked highly under the "'
    )
    print(
        '        "hybrid model while also maintaining close demographic KPI patterns."'
    )
    print("    ),")
    print("),")


if __name__ == "__main__":
    main()