import os
import time
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from google import genai


load_dotenv()

CACHE_DIR = Path("cache")
CACHE_PATH = CACHE_DIR / "embeddings.npy"


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in .env")

    return genai.Client(api_key=api_key)


def embed_texts(texts, model="gemini-embedding-001", batch_size=100, sleep_seconds=1):
    client = get_gemini_client()
    all_embeddings = []
    total = len(texts)

    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch = texts[start:end]

        print(f"Embedding batch {start} - {end} of {total}")

        response = client.models.embed_content(
            model=model,
            contents=batch,
        )

        batch_embeddings = [
            item.values
            for item in response.embeddings
        ]

        all_embeddings.extend(batch_embeddings)
        time.sleep(sleep_seconds)

    return np.array(all_embeddings, dtype="float32")


def load_or_create_embeddings(profiles, cache_path=CACHE_PATH):
    cache_path = Path(cache_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if cache_path.exists():
        print(f"Loading cached embeddings from {cache_path}")
        return np.load(cache_path)

    print("Generating Gemini embeddings...")

    embeddings = embed_texts(profiles)
    np.save(cache_path, embeddings)

    print(f"Saved embeddings to {cache_path}")

    return embeddings