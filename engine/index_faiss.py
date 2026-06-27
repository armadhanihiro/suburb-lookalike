import numpy as np
import faiss

def build_index(X):
    X = X.astype("float32")
    faiss.normalize_L2(X)
    index = faiss.IndexFlatIP(X.shape[1])
    index.add(X)
    return index

def nearest(index, X, row_idx, weights, n=10):
    q = (X[row_idx] * weights).astype("float32").reshape(1, -1)
    faiss.normalize_L2(q)
    sims, idx = index.search(q, n + 1)
    
    results = []
    for i, s in zip(idx[0], sims[0]):
        if i != row_idx:
            results.append((i, s))
        if len(results) == n:
            break
    return results