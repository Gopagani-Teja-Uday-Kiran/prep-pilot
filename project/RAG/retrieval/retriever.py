from functools import lru_cache
import os
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "rag" / "data" / "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "python_tutorial_314"
MIN_COSINE_SIMILARITY = float(
    os.getenv("RAG_MIN_COSINE_SIMILARITY", "0.35")
)


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=1)
def _get_collection():
    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"{CHROMA_DIR} not found. Build the index with "
            "rag/embeddings/embedder.py first."
        )

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_collection(name=COLLECTION_NAME)


def retrieve(query: str, top_k: int = 3) -> list[dict[str, object]]:
    collection = _get_collection()
    count = collection.count()
    if count == 0:
        return []

    query_embedding = _get_model().encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, count),
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0] or []
    metadatas = results["metadatas"][0] or []
    distances = results["distances"][0] or []
    matches = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        similarity = 1.0 - float(distance)
        if similarity < MIN_COSINE_SIMILARITY:
            continue

        matches.append({
            **(metadata or {}),
            "text": document,
            "score": similarity,
        })

    return matches