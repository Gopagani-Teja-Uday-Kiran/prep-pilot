import json
from pathlib import Path

from rag.retrieval.retriever import retrieve

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUESTIONS_PATH = PROJECT_ROOT / "rag" / "evaluation" / "questions.jsonl"
TOP_K = 3


def main() -> None:
    answerable_count = 0
    answerable_hits = 0
    unanswerable_count = 0
    correct_abstentions = 0

    with QUESTIONS_PATH.open(encoding="utf-8") as source:
        cases = [json.loads(line) for line in source if line.strip()]

    for case in cases:
        results = retrieve(case["question"], top_k=TOP_K)

        if case["answerable"]:
            answerable_count += 1
            hit = any(
                result.get("url") == case["expected_url"]
                for result in results
            )
            answerable_hits += int(hit)
        else:
            unanswerable_count += 1
            hit = not results
            correct_abstentions += int(hit)

            print(
            f"{case['id']}: "
            f"{'PASS' if hit else 'MISS'}; "
            f"retrieved {len(results)} chunks"
        )
        print("  matches:", [
            (result.get("url"), result.get("section"), round(float(result["score"]), 3))
            for result in results
        ])
    recall = answerable_hits / answerable_count if answerable_count else 0
    abstention_rate = (
        correct_abstentions / unanswerable_count if unanswerable_count else 0
    )

    print(f"\nRecall@{TOP_K}: {answerable_hits}/{answerable_count} ({recall:.1%})")
    print(
        "Correct abstention rate: "
        f"{correct_abstentions}/{unanswerable_count} ({abstention_rate:.1%})"
    )


if __name__ == "__main__":
    main()