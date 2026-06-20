from pathlib import Path

import faiss
import numpy as np


INDEX_PATH = Path("cache/faiss.index")


def l2_normalize(vectors):
    vectors = np.asarray(vectors, dtype=np.float32)

    norms = np.linalg.norm(
        vectors,
        axis=1,
        keepdims=True,
    )

    norms[norms == 0] = 1.0

    return vectors / norms


def build_faiss_index(vectors):
    """
    Build FAISS index using inner product over L2-normalized vectors.

    Inner product on normalized vectors is equivalent to cosine similarity.
    """
    vectors = l2_normalize(vectors)

    dimension = vectors.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    return index


def save_index(index, path=INDEX_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(path))


def load_index(path=INDEX_PATH):
    if not path.exists():
        return None

    return faiss.read_index(str(path))


def search_index(index, query_vector, top_n=10):
    query_vector = l2_normalize(query_vector)

    scores, indices = index.search(
        query_vector,
        top_n,
    )

    return scores[0], indices[0]