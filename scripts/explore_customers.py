from db.bigquery_client import get_bigquery_client

TABLE_NAME = "demografy.ref_tables.dev_customers"


def main():
    client = get_bigquery_client()
    table = client.get_table(TABLE_NAME)

    print("=== dev_customers schema ===")
    for field in table.schema:
        print(field.name, field.field_type)

    query = f"""
        SELECT *
        FROM `{TABLE_NAME}`
        LIMIT 5
    """

    df = client.query(query).to_dataframe()

    print("\n=== sample rows ===")
    print(df)


if __name__ == "__main__":
    main()