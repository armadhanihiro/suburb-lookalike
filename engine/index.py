from pathlib import Path
import faiss
import numpy as np

INDEX_PATH = Path("cache/faiss.index")

def build_faiss_index(vectors):
    """
    Build FAISS index from hybrid vectors.
    """

    vectors = np.asarray(vectors,dtype=np.float32,)
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
    query_vector = np.asarray(query_vector, dtype=np.float32,)
    scores, indices = index.search(query_vector.astype("float32"), top_n)

    return scores[0], indices[0]