def validate_embedding_cache(x_text):
    if x_text is None:
        return (
            False,
            "Gemini embedding cache is not available. "
            "Please run `python -m scripts.build_embeddings` first.",
        )

    return True, None


def validate_reference_index(reference_rows):
    if reference_rows.empty:
        return False, "Selected suburb was not found in the dataset."

    if len(reference_rows) > 1:
        return False, "Duplicate suburb display name found. Please check the dataset."

    return True, None


def validate_search_results(results):
    if not results:
        return False, "No similar suburbs were found for this reference."

    return True, None