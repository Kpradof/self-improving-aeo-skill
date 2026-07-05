# Experiment Program — Run 2 (real pages)

Run 2 upgrades the methodology after run 1's findings (see `experiments.md` → Run 1 summary). Three changes: real scraped pages, mean-of-3 gating, dual retrieval.

## What changed vs run 1

| Aspect | Run 1 | Run 2 |
|---|---|---|
| Corpus | 9 synthetic pages (same author) | 12+ real scraped pages, stratified by type, in `data-real/` (gitignored — copyrighted copies stay local) |
| Questions | Written by the harness author | Generated per page by an isolated agent that sees only the original page; spot-checked by a human |
| Gating | Single rewrite sample, keep if score > best | **Mean of 3 rewrite samples**, keep if mean > champion mean |
| Retrieval | Lexical only | **Lexical AND embedding** (`eval.py --retrieval embedding`); a rule is KEEP only if it does not lose in either mode |
| Rewriter | API (Opus) | Plan subagents (hybrid plan B) — the loop agent dispatches one isolated subagent per page with SYSTEM = harness constraints + SKILL.md; eval stays on the API (Haiku, deterministic, cached) |

## The loop (per experiment)

1. Read `experiments.md` history. One hypothesis, one change to `SKILL.md`.
2. Rewrite all dev pages **3 times** (3 independent samples — for subagent rewrites, dispatch 3 separate agents per page; for API rewrites, bust the cache by appending a blank line per sample).
3. For each sample, score with both retrievals:
   ```bash
   uv run --python 3.12 eval.py --root data-real --set dev --source rewritten --retrieval lexical
   uv run --python 3.12 eval.py --root data-real --set dev --source rewritten --retrieval embedding
   ```
4. Compute the mean per retrieval mode across the 3 samples.
5. KEEP only if: lexical mean > champion lexical mean AND embedding mean ≥ champion embedding mean (no regression). Otherwise REVERT.
6. Log means ± spread in `experiments.md`, commit/revert as in run 1.

## Question generation protocol

- One isolated agent per page: input = original page only; output = 8-10 Q&A pairs, questions phrased as a real user would search (paraphrase, never copy sentences), gold answers verbatim-extractable.
- The loop agent must not tailor SKILL.md rules to specific questions (same rule as run 1).
- Human spot-check of ~20% before freezing the corpus.

## Hard constraints (unchanged from run 1)

- Mutable file: `SKILL.md` only. Never touch `eval.py`, `rewrite.py`, `scrape.py`, `program*.md`, or anything under `data-real/`.
- Never read `data-real/holdout/` contents.
- Rules must be general — no page names, brands, or dataset numbers in SKILL.md.
- Holdout check once, at end of run, both retrieval modes.
