# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["anthropic"]
# ///
"""QA-based AEO eval simulating answer-engine retrieval.

Answer engines don't read whole pages — they retrieve a fragment and answer
from it. So: each page is split into ~120-word chunks; for each question,
the chunk with the highest lexical overlap is retrieved, and a small model
(Haiku) answers using ONLY that chunk. If the fact is buried in meandering
prose, separated from its subject, or under an unrelated heading, retrieval
or extraction fails — exactly the failure mode AEO rewriting must fix.

FIXED FILE — the experiment agent must never modify this script.
"""

import argparse
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic

REPO = Path(__file__).parent


def load_dotenv() -> None:
    env_file = REPO / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


load_dotenv()
READER_MODEL = "claude-haiku-4-5"
JUDGE_MODEL = "claude-haiku-4-5"

READER_SYSTEM = (
    "You answer questions using ONLY the document excerpt provided by the user. "
    "Answer with one short phrase — no explanation, no preamble. "
    "Do not guess or infer beyond what the excerpt states. "
    "If the excerpt does not clearly contain the answer, reply exactly: NOT_FOUND"
)

CHUNK_WORDS = 120

STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "on", "at", "for", "and", "or", "is",
    "are", "was", "does", "do", "did", "what", "which", "who", "when", "where",
    "how", "why", "much", "many", "long", "with", "that", "this", "it", "its",
    "by", "from", "can", "per", "s",
}


def chunk_page(text: str) -> list[str]:
    """Split a page into chunks of at most ~CHUNK_WORDS words along paragraphs."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    count = 0
    for para in paragraphs:
        words = para.split()
        if len(words) >= CHUNK_WORDS:
            if current:
                chunks.append("\n\n".join(current))
                current, count = [], 0
            for i in range(0, len(words), CHUNK_WORDS):
                chunks.append(" ".join(words[i:i + CHUNK_WORDS]))
            continue
        if count + len(words) > CHUNK_WORDS and current:
            chunks.append("\n\n".join(current))
            current, count = [], 0
        current.append(para)
        count += len(words)
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def tokenize(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9$%']+", text.lower()) if w not in STOPWORDS}


def retrieve_chunk(chunks: list[str], question: str) -> str:
    """Naive lexical retrieval: chunk with the most question-word overlap wins."""
    q_words = tokenize(question)
    return max(chunks, key=lambda c: len(q_words & tokenize(c)))

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


def grade_question(client: anthropic.Anthropic, chunks: list[str], q: dict) -> bool:
    excerpt = retrieve_chunk(chunks, q["q"])
    answer_resp = client.messages.create(
        model=READER_MODEL,
        max_tokens=100,
        temperature=0,
        system=READER_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": f"<excerpt>\n{excerpt}\n</excerpt>\n\nQuestion: {q['q']}",
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
    chunks = chunk_page(doc_path.read_text())
    questions = json.loads((page_dir / "questions.json").read_text())["questions"]
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda q: grade_question(client, chunks, q), questions))
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
