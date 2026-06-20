TIER_LIMITS = {
    "Free": 5,
    "Basic": 10,
    "Pro": 25,
}


MOCK_USERS = {
    "user_017": {
        "tier": "Pro",
        "lookups_used": 8,
        "lookup_limit": 50,
    },
    "user_001": {
        "tier": "Free",
        "lookups_used": 2,
        "lookup_limit": 10,
    },
}


def get_user_access(user_id):
    user = MOCK_USERS.get(
        user_id,
        {
            "tier": "Free",
            "lookups_used": 0,
            "lookup_limit": 10,
        },
    )

    tier = user["tier"]

    return {
        "user_id": user_id,
        "tier": tier,
        "lookups_used": user["lookups_used"],
        "lookup_limit": user["lookup_limit"],
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