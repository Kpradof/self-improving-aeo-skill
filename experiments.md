# Experiment Log

Metric: QA accuracy on `data/dev/` (fraction of questions a small model answers correctly from the rewritten page).

Eval simulates answer-engine retrieval: page split into ~120-word chunks, best-matching chunk retrieved per question, Haiku answers from that chunk only.

| # | Hypothesis | Score | Δ vs best | Verdict | Insight |
|---|-----------|-------|-----------|---------|---------|
| B0 | Baseline: original pages, no rewrite | 66.7% (32/48) | — | — | Buried facts + pronouns without antecedents kill snippet retrieval |
| B1 | SKILL.md v0: preserve facts + clear prose only | 72.9% (35/48) | +6.2 | KEEP (initial) | Even generic "clear prose" helps; pages 01 & 05 (4/8) are where the headroom lives |
| 01 | Self-contained sentences: name entity explicitly, no pronouns | 79.2% (38/48) | +6.3 | KEEP | Big lift on product/pricing pages (01: 4→7, 04: 8/8); narrative blog (03) dropped 8→4 — entity naming may not fix story-style prose |
| 02 | Question-shaped headings sharing query vocabulary | 83.3% (40/48) | +4.1 | KEEP | Headings act as retrieval anchors; narrative page (03) recovered 4→7, event page (05) 6/8 |
| 03 | Answer-first: first sentence under heading fully answers it | 81.2% (39/48) | -2.1 | REVERT | Page 03 dropped again (7→4); compressing answers up top may strip surrounding keywords retrieval needs |
| 04 | FAQ section restating key facts as Q&A pairs | 83.3% (40/48) | 0.0 | REVERT | Neutral: FAQ chunk competes with body chunk for retrieval, splitting keyword mass instead of adding coverage |
| 05 | Short single-topic paragraphs (max 3 sentences) | 77.1% (37/48) | -6.2 | REVERT | Surprising: fragmenting hurts — tiny paragraphs get grouped into chunks with weaker per-question keyword density |
