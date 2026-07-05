# Experiment Log

Metric: QA accuracy on `data/dev/` (fraction of questions a small model answers correctly from the rewritten page).

Eval simulates answer-engine retrieval: page split into ~120-word chunks, best-matching chunk retrieved per question, Haiku answers from that chunk only.

| # | Hypothesis | Score | Δ vs best | Verdict | Insight |
|---|-----------|-------|-----------|---------|---------|
| B0 | Baseline: original pages, no rewrite | 66.7% (32/48) | — | — | Buried facts + pronouns without antecedents kill snippet retrieval |
| B1 | SKILL.md v0: preserve facts + clear prose only | 72.9% (35/48) | +6.2 | KEEP (initial) | Even generic "clear prose" helps; pages 01 & 05 (4/8) are where the headroom lives |
