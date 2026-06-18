import numpy as np

from engine.similarity import find_similar_suburbs


def test_find_similar_suburbs_returns_top_n():
    X = np.array([
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.9, 0.1],
        [0.0, 0.0, 1.0],
    ])

    results = find_similar_suburbs(X, reference_idx=0, top_n=2)

    assert len(results) == 2
    assert results[0]["index"] == 1
    assert results[0]["similarity"] > results[1]["similarity"]
    assert results[0]["similarity"] <= 1.0
    assert results[1]["similarity"] >= 0.0
