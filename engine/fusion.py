import numpy as np
from sklearn.preprocessing import normalize


def fuse_vectors(X_numeric, X_text, alpha=0.4):
    """
    Fuse numeric KPI vectors and text embedding vectors.

    alpha = 0.0 -> numeric only
    alpha = 1.0 -> text only
    alpha = 0.4 -> 60% numeric, 40% text
    """

    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be between 0 and 1")

    if X_numeric.shape[0] != X_text.shape[0]:
        raise ValueError(   
            "Numeric and text matrices must have the same number of rows"
        )

    X_numeric_norm = normalize(X_numeric)
    X_text_norm = normalize(X_text)

    hybrid_vectors = np.hstack(
        [
            (1 - alpha) * X_numeric_norm,
            alpha * X_text_norm,
        ]
    )

    return hybrid_vectors.astype("float32")