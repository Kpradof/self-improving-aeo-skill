# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["anthropic"]
# ///
"""Apply the rules in SKILL.md to every page in a dataset.

FIXED FILE — the experiment agent must never modify this script.
The only lever in the loop is the content of SKILL.md.
"""

import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic

REPO = Path(__file__).parent
REWRITER_MODEL = os.environ.get("AEO_REWRITER_MODEL", "claude-opus-4-8")

# Hard constraints live here, outside SKILL.md, so no mutation can relax them.
SYSTEM_TEMPLATE = """You rewrite web pages following the rewrite rules provided below.

HARD CONSTRAINTS (these override anything in the rules):
- Preserve every fact from the original page exactly: names, numbers, dates, prices, percentages, URLs. Never invent, alter, or drop a fact.
- Do not fabricate content that is not supported by the original page.
- Output ONLY the rewritten page as markdown. No preamble, no commentary, no code fences around the whole page.

REWRITE RULES:
<rules>
{rules}
</rules>"""


def rewrite_page(client: anthropic.Anthropic, system: str, page_dir: Path, out_dir: Path) -> str:
    original = (page_dir / "original.md").read_text()
    response = client.messages.create(
        model=REWRITER_MODEL,
        max_tokens=4000,
        system=system,
        messages=[
            {
                "role": "user",
                "content": f"Rewrite this page:\n\n{original}",
            }
        ],
    )
    text = next(b.text for b in response.content if b.type == "text")
    out_page = out_dir / page_dir.name
    out_page.mkdir(parents=True, exist_ok=True)
    (out_page / "rewritten.md").write_text(text)
    return page_dir.name


def main() -> None:
    parser = argparse.ArgumentParser(description="Rewrite pages using SKILL.md rules")
    parser.add_argument("--set", dest="dataset", choices=["dev", "holdout"], default="dev")
    args = parser.parse_args()

    rules = (REPO / "SKILL.md").read_text()
    system = SYSTEM_TEMPLATE.format(rules=rules)

    data_dir = REPO / "data" / args.dataset
    out_dir = REPO / "output" / args.dataset
    page_dirs = sorted(p for p in data_dir.iterdir() if p.is_dir())
    if not page_dirs:
        sys.exit(f"No pages found in {data_dir}")

    client = anthropic.Anthropic()
    print(f"Rewriting {len(page_dirs)} pages ({args.dataset}) with {REWRITER_MODEL}...")
    with ThreadPoolExecutor(max_workers=4) as pool:
        for name in pool.map(lambda p: rewrite_page(client, system, p, out_dir), page_dirs):
            print(f"  done: {name}")
    print(f"Rewritten pages in {out_dir}")


if __name__ == "__main__":
    main()
