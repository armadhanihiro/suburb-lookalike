from pathlib import Path

from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from engine.text_embed import load_or_create_embeddings
from engine.fusion import fuse_vectors
from engine.similarity import find_similar_suburbs
from eval.golden_set import GOLDEN_SET


ALPHAS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
TOP_K_VALUES = [3, 5, 10]
CACHE_PATH = "cache/suburb_embeddings.npy"
REPORT_PATH = Path("eval/alpha_sweep_report.md")


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


def evaluate_alpha(df, x_numeric, x_text, all_keys, alpha):
    x_hybrid = fuse_vectors(
        x_numeric,
        x_text,
        alpha=alpha,
    )

    scores = {
        k: {
            "precision": [],
            "recall": [],
        }
        for k in TOP_K_VALUES
    }

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

        for k in TOP_K_VALUES:
            scores[k]["precision"].append(
                precision_at_k(predicted, expected, k)
            )
            scores[k]["recall"].append(
                recall_at_k(predicted, expected, k)
            )

    averages = {}

    for k in TOP_K_VALUES:
        averages[f"p@{k}"] = (
            sum(scores[k]["precision"]) / len(scores[k]["precision"])
        )
        averages[f"r@{k}"] = (
            sum(scores[k]["recall"]) / len(scores[k]["recall"])
        )

    return averages


def main():
    client = get_bigquery_client()
    df, x_numeric, _ = load_suburb_data(client)

    x_text = load_or_create_embeddings(
        profiles=[],
        cache_path=CACHE_PATH,
    )

    all_keys = df.apply(make_key, axis=1).tolist()

    rows = []

    print("=== Alpha Sweep Evaluation ===")
    print(f"Golden references: {len(GOLDEN_SET)}")
    print("")

    for alpha in ALPHAS:
        result = evaluate_alpha(
            df=df,
            x_numeric=x_numeric,
            x_text=x_text,
            all_keys=all_keys,
            alpha=alpha,
        )

        result["alpha"] = alpha
        rows.append(result)

        print(
            f"alpha={alpha:.1f} | "
            f"P@3={result['p@3']:.3f} "
            f"P@5={result['p@5']:.3f} "
            f"P@10={result['p@10']:.3f} | "
            f"R@3={result['r@3']:.3f} "
            f"R@5={result['r@5']:.3f} "
            f"R@10={result['r@10']:.3f}"
        )

    markdown_lines = [
        "# Alpha Sweep Evaluation Report",
        "",
        f"Golden references: {len(GOLDEN_SET)}",
        "",
        "| Alpha | P@3 | P@5 | P@10 | R@3 | R@5 | R@10 |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in rows:
        markdown_lines.append(
            f"| {row['alpha']:.1f} | "
            f"{row['p@3']:.3f} | "
            f"{row['p@5']:.3f} | "
            f"{row['p@10']:.3f} | "
            f"{row['r@3']:.3f} | "
            f"{row['r@5']:.3f} | "
            f"{row['r@10']:.3f} |"
        )

    markdown_lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Alpha controls the balance between numeric KPI similarity and text embedding similarity.",
            "- Alpha 0.0 represents numeric-only similarity.",
            "- Alpha 1.0 represents text-only similarity.",
            "- The selected default alpha should balance precision and recall while keeping rankings stable.",
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