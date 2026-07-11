from db.bigquery_client import get_bigquery_client
from engine.features import load_suburb_data
from eval.golden_set import GOLDEN_SET


def make_key(row):
    return f"{row['sa2_name']} - {row['state']}"


def main():
    client = get_bigquery_client()
    df, _, _ = load_suburb_data(client)

    dataset_keys = set(
        df.apply(make_key, axis=1)
    )

    errors = 0

    print("=== Validate Golden Set ===\n")

    for item in GOLDEN_SET:
        print(f"Reference: {item.reference}")

        if item.reference not in dataset_keys:
            print(f"Reference not found: {item.reference}")
            errors += 1
        else:
            print("Reference found")

        for expected in item.expected:
            if expected not in dataset_keys:
                print(f"Expected not found: {expected}")
                errors += 1

        print("")

    if errors == 0:
        print("Golden set is valid.")
    else:
        print(f"Found {errors} invalid suburb name(s).")


if __name__ == "__main__":
    main()