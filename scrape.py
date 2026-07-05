# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["trafilatura"]
# ///
"""Fetch real web pages and store them as markdown-ish text for run 2.

Usage:
    uv run scrape.py --url https://example.com/pricing --set dev --name page-01

Pages land in data-real/<set>/<name>/original.md (data-real/ is gitignored —
third-party page copies stay local, only aggregate results are published).
"""

import argparse
import sys
from pathlib import Path

import trafilatura

REPO = Path(__file__).parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a real page into the run-2 corpus")
    parser.add_argument("--url", required=True)
    parser.add_argument("--set", dest="dataset", choices=["dev", "holdout"], required=True)
    parser.add_argument("--name", required=True, help="page directory name, e.g. page-01")
    args = parser.parse_args()

    downloaded = trafilatura.fetch_url(args.url)
    if not downloaded:
        sys.exit(f"Could not fetch {args.url}")
    text = trafilatura.extract(
        downloaded, include_links=False, include_tables=True, output_format="markdown"
    )
    if not text or len(text.split()) < 120:
        sys.exit(f"Extraction too short for {args.url} — page may be JS-only")

    page_dir = REPO / "data-real" / args.dataset / args.name
    page_dir.mkdir(parents=True, exist_ok=True)
    (page_dir / "original.md").write_text(text)
    (page_dir / "source.txt").write_text(args.url + "\n")
    print(f"{args.name}: {len(text.split())} words <- {args.url}")


if __name__ == "__main__":
    main()
