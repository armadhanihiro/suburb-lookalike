import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# 1. 定义 KPI 名称（必须和特征矩阵列顺序一致）
# ============================================================
KPI_NAMES = [
    "kpi_1_val", "kpi_2_val", "kpi_3_val", "kpi_4_val", "kpi_5_val",
    "kpi_6_val", "kpi_7_val", "kpi_8_val", "kpi_9_val", "kpi_10_val"
]

# ============================================================
# 2. Weighting（1.0 = normal, >1 more important, <1 less important）
# ============================================================
KPI_WEIGHTS = {
    "kpi_1_val": 1.2,   # Prosperity Score
    "kpi_2_val": 1.2,   # Diversity Index
    "kpi_3_val": 0.6,   # Migration Footprint
    "kpi_4_val": 1.0,   # Learning Level
    "kpi_5_val": 0.9,   # Social Housing
    "kpi_6_val": 0.8,   # Resident Equity
    "kpi_7_val": 1.1,   # Rental Access
    "kpi_8_val": 0.9,   # Resident Anchor
    "kpi_9_val": 1.2,   # Household Mobility Potential
    "kpi_10_val": 1.1,  # Young Family Indicator
}

# ============================================================
# 3. Applying weights to the feature matrix
# ============================================================
def apply_weights(X, weight_dict=None):
    """X: 标准化后的特征矩阵 (n_suburbs × n_kpi)"""
    if weight_dict is None:
        weight_dict = KPI_WEIGHTS
    w = np.array([weight_dict.get(name, 1.0) for name in KPI_NAMES])
    return X * w

# ============================================================
# 4. Core：Similar Suburbs + return 0–100 similarity scores
# ============================================================
def find_similar_suburbs(X, selected_idx, top_n=10, use_weights=True, weight_dict=None):
    """
    参数:
        X: 标准化特征矩阵
        selected_idx: 选中郊区的行号
        top_n: 返回数量
        use_weights: 是否启用权重
        weight_dict: 自定义权重字典
    返回:
        indices: 相似郊区的行号（numpy array）
        scores_0_100: 0–100 的相似度分数（越高越像）
    """
    if use_weights:
        X_processed = apply_weights(X, weight_dict)
    else:
        X_processed = X

    sim = cosine_similarity(X_processed[selected_idx:selected_idx+1], X_processed)[0]
    sim[selected_idx] = -1
    top_indices = np.argsort(sim)[::-1][:top_n]
    top_sim = sim[top_indices]
    scores_0_100 = (top_sim + 1) / 2 * 100
    return top_indices, scores_0_100


# ============================================================
# 5. 可选：返回哪些 KPI 贡献最大（解释性）
# ============================================================
def explain_top_contributors(X, source_idx, target_idx, top_k=3):
    """
    简单版本：通过特征差值的绝对值来找出哪些 KPI 最相似 / 最不同
    """
    diff = np.abs(X[source_idx] - X[target_idx])
    top_feature_indices = np.argsort(diff)[::-1][:top_k]
    top_feature_names = [KPI_NAMES[i] for i in top_feature_indices]
    top_diffs = diff[top_feature_indices]
    return top_feature_names, top_diffs