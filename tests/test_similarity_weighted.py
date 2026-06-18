import numpy as np

from similarity_weighted import find_similar_suburbs


def test_weighted_similarity_returns_expected_shape():
    X = np.array([
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ])

    indices, scores = find_similar_suburbs(X, 0, top_n=3, use_weights=False)
    assert len(indices) == 3
    assert len(scores) == 3
    assert 0 <= scores.min() <= 100
    assert 0 <= scores.max() <= 100

    weights = {
        "kpi_1_val": 0.1,
        "kpi_2_val": 2.0,
        "kpi_3_val": 1.0,
        "kpi_4_val": 1.0,
        "kpi_5_val": 1.0,
        "kpi_6_val": 1.0,
        "kpi_7_val": 1.0,
        "kpi_8_val": 1.0,
        "kpi_9_val": 1.0,
        "kpi_10_val": 1.0,
    }
    weighted_indices, weighted_scores = find_similar_suburbs(
        X,
        0,
        top_n=3,
        use_weights=True,
        weight_dict=weights,
    )
    assert len(weighted_indices) == 3
    assert len(weighted_scores) == 3
    assert 0 <= weighted_scores.min() <= 100
    assert 0 <= weighted_scores.max() <= 100
    assert not np.array_equal(weighted_scores, scores) or not np.array_equal(weighted_indices, indices)
