import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_suburbs(X, reference_idx, top_n=10):
    query_vector = X[reference_idx].reshape(1, -1)
    similarities = cosine_similarity(query_vector, X)[0]
    similarities[reference_idx] = -1
    top_indices = np.argsort(similarities)[::-1][:top_n]

    return [
        {
            "index": int(idx),
            "similarity": float(similarities[idx])
        }
        for idx in top_indices
    ]  