from pathlib import Path

from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.text_embed import load_or_create_embeddings
from engine.fusion import fuse_vectors
from engine.similarity import find_similar_suburbs
from eval.golden_set import GOLDEN_SET


ALPHA = 0.4
TOP_K_VALUES = [3, 5, 10]
CACHE_PATH = "cache/suburb_embeddings.npy"
REPORT_PATH = Path("eval/evaluation_report.md")


def make_key(row):
    return f"{row['sa2_name']} - {row['state']}"


def precision_at_k(predicted, expected, k):
    predicted_k = predicted[:k]
    hits = len(set(predicted_k) & set(expected))
    return hits / k


def recall_at_k(predicted, expected, k):
    predicted_k = predicted[:k]
    hits = len(set(predicted_k) & set(expected))
    return hits / len(expected)


def main():
    client = get_bigquery_client()
    df, x_numeric, _ = load_suburb_data(client)

    x_text = load_or_create_embeddings(
        profiles=[],
        cache_path=CACHE_PATH,
    )

    x_hybrid = fuse_vectors(
        x_numeric,
        x_text,
        alpha=ALPHA,
    )

    all_keys = df.apply(make_key, axis=1).tolist()

    scores = {
        k: {
            "precision": [],
            "recall": [],
        }
        for k in TOP_K_VALUES
    }

    report_rows = []

    print("=== Golden Set Evaluation ===")
    print(f"Alpha: {ALPHA}")
    print(f"Golden references: {len(GOLDEN_SET)}")
    print("")

    for item in GOLDEN_SET:
        reference_idx = all_keys.index(item.reference)

        results = find_similar_suburbs(
            x_hybrid,
            reference_idx,
            top_n=max(TOP_K_VALUES),
        )

        predicted = [
            make_key(df.iloc[result["index"]])
            for result in results
        ]

        expected = item.expected

        print(f"Reference: {item.reference}")
        print(f"Rationale: {item.rationale}")

        row = {
            "reference": item.reference,
        }

        for k in TOP_K_VALUES:
            precision = precision_at_k(
                predicted,
                expected,
                k,
            )

            recall = recall_at_k(
                predicted,
                expected,
                k,
            )

            scores[k]["precision"].append(precision)
            scores[k]["recall"].append(recall)

            row[f"p@{k}"] = precision
            row[f"r@{k}"] = recall

            print(
                f"  Precision@{k}: {precision:.3f} | "
                f"Recall@{k}: {recall:.3f}"
            )

        report_rows.append(row)
        print("")

    print("=== Average Scores ===")

    averages = {}

    for k in TOP_K_VALUES:
        avg_precision = (
            sum(scores[k]["precision"]) / len(scores[k]["precision"])
        )
        avg_recall = (
            sum(scores[k]["recall"]) / len(scores[k]["recall"])
        )

        averages[f"p@{k}"] = avg_precision
        averages[f"r@{k}"] = avg_recall

        print(
            f"Precision@{k}: {avg_precision:.3f} | "
            f"Recall@{k}: {avg_recall:.3f}"
        )

    print("")
    print("=== Summary Table ===")
    print(
        f"{'Reference':<45} "
        f"{'P@3':>6} {'P@5':>6} {'P@10':>6} "
        f"{'R@3':>6} {'R@5':>6} {'R@10':>6}"
    )

    markdown_lines = [
        "# Golden Set Evaluation Report",
        "",
        f"Alpha: {ALPHA}",
        f"Golden references: {len(GOLDEN_SET)}",
        "",
        "| Reference | P@3 | P@5 | P@10 | R@3 | R@5 | R@10 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for row in report_rows:
        print(
            f"{row['reference']:<45} "
            f"{row['p@3']:>6.3f} "
            f"{row['p@5']:>6.3f} "
            f"{row['p@10']:>6.3f} "
            f"{row['r@3']:>6.3f} "
            f"{row['r@5']:>6.3f} "
            f"{row['r@10']:>6.3f}"
        )

        markdown_lines.append(
            f"| {row['reference']} | "
            f"{row['p@3']:.3f} | "
            f"{row['p@5']:.3f} | "
            f"{row['p@10']:.3f} | "
            f"{row['r@3']:.3f} | "
            f"{row['r@5']:.3f} | "
            f"{row['r@10']:.3f} |"
        )

    markdown_lines.append(
        f"| **Average** | "
        f"**{averages['p@3']:.3f}** | "
        f"**{averages['p@5']:.3f}** | "
        f"**{averages['p@10']:.3f}** | "
        f"**{averages['r@3']:.3f}** | "
        f"**{averages['r@5']:.3f}** | "
        f"**{averages['r@10']:.3f}** |"
    )

    markdown_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Precision measures how many returned suburbs were expected neighbours.",
            "- Recall measures how many expected neighbours were successfully retrieved.",
            "- Precision usually decreases as K increases because more results are included.",
            "- Recall usually increases as K increases because the model has more chances to retrieve expected neighbours.",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(markdown_lines),
        encoding="utf-8",
    )

    print("")
    print(f"Report saved to {REPORT_PATH}")


if __name__ == "__main__":
    main()