import hashlib
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "rag" / "data" / "python_tutorial_sections.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "rag" / "data" / "python_tutorial_chunks.jsonl"

CHUNK_WORDS = 350
OVERLAP_WORDS = 50


def make_chunks(record: dict[str, str]) -> list[dict[str, object]]:
    words = record["text"].split()
    step = CHUNK_WORDS - OVERLAP_WORDS
    chunks = []

    for index, start in enumerate(range(0, len(words), step)):
        text = " ".join(words[start:start + CHUNK_WORDS])
        if not text:
            continue

        chunk_id = hashlib.sha256(
            f"{record['url']}|{record['section']}|{index}|{text}".encode("utf-8")
        ).hexdigest()

        chunks.append({
            **record,
            "chunk_id": chunk_id,
            "chunk_index": index,
            "text": text,
        })

        if start + CHUNK_WORDS >= len(words):
            break

    return chunks


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"{INPUT_PATH} not found. Run the ingestion script first."
        )

    chunks = []
    with INPUT_PATH.open(encoding="utf-8") as source:
        for line in source:
            chunks.extend(make_chunks(json.loads(line)))

    with OUTPUT_PATH.open("w", encoding="utf-8") as output:
        for chunk in chunks:
            output.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"Saved {len(chunks)} chunks to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()