# Experiment Log

Metric: QA accuracy on `data/dev/` (fraction of questions a small model answers correctly from the rewritten page).

Eval simulates answer-engine retrieval: page split into ~120-word chunks, best-matching chunk retrieved per question, Haiku answers from that chunk only.

| # | Hypothesis | Score | Δ vs best | Verdict | Insight |
|---|-----------|-------|-----------|---------|---------|
| B0 | Baseline: original pages, no rewrite | 66.7% (32/48) | — | — | Buried facts + pronouns without antecedents kill snippet retrieval |
| B1 | SKILL.md v0: preserve facts + clear prose only | 72.9% (35/48) | +6.2 | KEEP (initial) | Even generic "clear prose" helps; pages 01 & 05 (4/8) are where the headroom lives |
| 01 | Self-contained sentences: name entity explicitly, no pronouns | 79.2% (38/48) | +6.3 | KEEP | Big lift on product/pricing pages (01: 4→7, 04: 8/8); narrative blog (03) dropped 8→4 — entity naming may not fix story-style prose |
