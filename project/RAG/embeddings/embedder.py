import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "rag" / "data"
CHUNKS_PATH = DATA_DIR / "python_tutorial_chunks.jsonl"
CHROMA_DIR = DATA_DIR / "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "python_tutorial_314"
CORPUS_NAME = "python-tutorial-3.14"


def main() -> None:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"{CHUNKS_PATH} not found. Run ingestion and chunking first."
        )

    with CHUNKS_PATH.open(encoding="utf-8") as source:
        chunks = [json.loads(line) for line in source if line.strip()]

    if not chunks:
        raise ValueError(f"No chunks found in {CHUNKS_PATH}")
    unique_chunks = {}
    for chunk in chunks:
        unique_chunks.setdefault(str(chunk["chunk_id"]), chunk)

    if len(unique_chunks) < len(chunks):
        print(f"Skipped {len(chunks) - len(unique_chunks)} duplicate chunks")

    chunks = list(unique_chunks.values())   

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(
        [chunk["text"] for chunk in chunks],
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    collection.delete(where={"corpus": CORPUS_NAME})

    metadatas = []
    for chunk in chunks:
        metadatas.append({
            "corpus": CORPUS_NAME,
            "title": str(chunk["title"]),
            "url": str(chunk["url"]),
            "section": str(chunk["section"]),
            "version": str(chunk["version"]),
            "license": str(chunk["license"]),
            "accessed_at": str(chunk["accessed_at"]),
            "chunk_index": int(chunk["chunk_index"]),
        })

    collection.upsert(
        ids=[str(chunk["chunk_id"]) for chunk in chunks],
        documents=[str(chunk["text"]) for chunk in chunks],
        metadatas=metadatas,
        embeddings=embeddings.tolist(),
    )

    print(f"Indexed {len(chunks)} chunks in {CHROMA_DIR}")


if __name__ == "__main__":
    main()