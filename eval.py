# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
"""QA-based AEO eval: a small model reads each page and answers factual
questions; answers are graded against gold answers.

FIXED FILE — the experiment agent must never modify this script.

The reader is deliberately a small model (Haiku): if a weak reader can
extract the right answers, the page is genuinely AI-readable.
"""

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic

REPO = Path(__file__).parent
READER_MODEL = "claude-haiku-4-5"
JUDGE_MODEL = "claude-haiku-4-5"

READER_SYSTEM = (
    "You answer questions using ONLY the document provided by the user. "
    "Answer with one short phrase — no explanation, no preamble. "
    "If the document does not contain the answer, reply exactly: NOT_FOUND"
)

JUDGE_SYSTEM = (
    "You grade whether a candidate answer conveys the same fact as the gold answer. "
    "Mark correct=true only if the candidate states the same fact (wording may differ, "
    "units/formatting may differ if the value is the same). "
    "NOT_FOUND, a contradiction, or a different value is correct=false."
)

JUDGE_SCHEMA = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {"correct": {"type": "boolean"}},
        "required": ["correct"],
        "additionalProperties": False,
    },
}


def grade_question(client: anthropic.Anthropic, document: str, q: dict) -> bool:
    answer_resp = client.messages.create(
        model=READER_MODEL,
        max_tokens=100,
        temperature=0,
        system=READER_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": f"<document>\n{document}\n</document>\n\nQuestion: {q['q']}",
            }
        ],
    )
    candidate = next(b.text for b in answer_resp.content if b.type == "text").strip()

    judge_resp = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=50,
        temperature=0,
        system=JUDGE_SYSTEM,
        output_config={"format": JUDGE_SCHEMA},
        messages=[
            {
                "role": "user",
                "content": (
                    f"Question: {q['q']}\n"
                    f"Gold answer: {q['gold']}\n"
                    f"Candidate answer: {candidate}"
                ),
            }
        ],
    )
    verdict = json.loads(next(b.text for b in judge_resp.content if b.type == "text"))
    return bool(verdict["correct"])


def eval_page(client: anthropic.Anthropic, page_dir: Path, doc_path: Path) -> tuple[str, int, int]:
    document = doc_path.read_text()
    questions = json.loads((page_dir / "questions.json").read_text())["questions"]
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda q: grade_question(client, document, q), questions))
    return page_dir.name, sum(results), len(results)


def main() -> None:
    parser = argparse.ArgumentParser(description="Grade pages via QA accuracy")
    parser.add_argument("--set", dest="dataset", choices=["dev", "holdout"], default="dev")
    parser.add_argument(
        "--source",
        choices=["rewritten", "original"],
        default="rewritten",
        help="'original' scores the raw pages (baseline); 'rewritten' scores output/<set>/",
    )
    args = parser.parse_args()

    data_dir = REPO / "data" / args.dataset
    page_dirs = sorted(p for p in data_dir.iterdir() if p.is_dir())
    if not page_dirs:
        sys.exit(f"No pages found in {data_dir}")

    client = anthropic.Anthropic()
    per_page = {}
    total_correct = 0
    total_questions = 0

    for page_dir in page_dirs:
        if args.source == "original":
            doc_path = page_dir / "original.md"
        else:
            doc_path = REPO / "output" / args.dataset / page_dir.name / "rewritten.md"
            if not doc_path.exists():
                sys.exit(f"Missing {doc_path} — run rewrite.py --set {args.dataset} first")
        name, correct, n = eval_page(client, page_dir, doc_path)
        per_page[name] = f"{correct}/{n}"
        total_correct += correct
        total_questions += n
        print(f"  {name}: {correct}/{n}")

    overall = total_correct / total_questions
    print(f"\nOverall accuracy ({args.dataset}, {args.source}): "
          f"{total_correct}/{total_questions} = {overall:.1%}")
    print("RESULT " + json.dumps({
        "set": args.dataset,
        "source": args.source,
        "overall": round(overall, 4),
        "pages": per_page,
    }))


if __name__ == "__main__":
    main()
