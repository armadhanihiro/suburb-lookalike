from google.cloud import bigquery


TIER_LIMITS = {
    "free": 5,
    "basic": 10,
    "pro": 25,
}

LOOKUP_LIMITS = {
    "free": 5,
    "basic": 20,
    "pro": 50,
}

CUSTOMERS_TABLE = "demografy.ref_tables.dev_customers"


def normalize_tier(tier):
    if not tier:
        return "free"

    return str(tier).strip().lower()


def get_customer_from_bigquery(client, login_id):
    login_id = str(login_id).strip().lower()

    query = f"""
        SELECT
            user_id,
            email,
            tier,
            is_active
        FROM `{CUSTOMERS_TABLE}`
        WHERE LOWER(TRIM(user_id)) = @login_id
           OR LOWER(TRIM(email)) = @login_id
        LIMIT 1
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "login_id",
                "STRING",
                login_id,
            )
        ]
    )

    df = client.query(
        query,
        job_config=job_config,
    ).to_dataframe()

    if df.empty:
        return None

    return df.iloc[0].to_dict()


def get_user_access(login_id, client=None):
    login_id = str(login_id).strip()

    if client is None:
        return None

    customer = get_customer_from_bigquery(
        client,
        login_id,
    )

    if customer is None:
        return None

    return build_access(
        user_id=customer["user_id"],
        tier=customer["tier"],
        is_active=customer["is_active"],
    )


def build_access(user_id, tier, is_active=True, lookups_used=0):
    tier = normalize_tier(tier)

    return {
        "user_id": user_id,
        "tier": tier.title(),
        "is_active": bool(is_active),
        "lookups_used": lookups_used,
        "lookup_limit": LOOKUP_LIMITS.get(tier, 10),
        "match_cap": TIER_LIMITS.get(tier, 5),
    }


def cap_top_n(top_n, access):
    return min(top_n, access["match_cap"])


def increment_lookup(access):
    updated_access = access.copy()
    updated_access["lookups_used"] += 1
    return updated_access


def has_lookup_remaining(access):
    return access["lookups_used"] < access["lookup_limit"]