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
| 06 | Mirror plain query vocabulary next to every fact | 81.2% (39/48) | -2.1 | REVERT | Below best despite per-page gains on 01/05 — rewrite variance is real (~±2 pts); single-rule deltas under ~3 pts are noise |
| 07 | Cut factless marketing filler (page may shrink to 50%) | 83.3% (40/48) | 0.0 | REVERT | Tie — fluff removal helps density but loses incidental keyword matches; net zero |
| 08 | Minimal intro, topic vocabulary only in its own section | 79.2% (38/48) | -4.1 | REVERT | Right diagnosis (intro steals retrieval) but negative-space rule executed inconsistently by rewriter |
| 09 | Stack topic terms in heading AND fact sentence | 75.0% (36/48) | -8.3 | REVERT | Backfired: stacking everywhere creates keyword collisions between sections; retrieval margin needs contrast, not global density |
| 10 | Enumerable facts as tables/bullets, one complete fact per row | 85.4% (41/48) | +2.1 | KEEP | Rows are naturally self-contained retrieval units; first KEEP since exp02 |
| 11 | Plain search vocabulary in rows/headings (scoped exp06 retry) | 79.2% (38/48) | -6.2 | REVERT | Vocabulary substitution keeps hurting page 03 (narrative); rewriter strips story keywords questions rely on |
| 12 | Keep original terminology, reorganize only | 79.2% (38/48) | -6.2 | REVERT | 'Don't reword' constrains the rewriter's wins from rules 4-6 more than it protects page 03 |
| 13 | Canonical question checklist + qualifiers in rows (bundled — mistake) | 83.3% (40/48) | -2.1 | REVERT | Pages 01-02 hit 8/8 but 05-06 dropped: flooding pages with question-headings recreates collisions. Unbundle next |
| 14 | Keep qualifiers attached to values in rows (unbundled from exp13) | 87.5% (42/48) | +2.1 | KEEP | Page 06 8/8: 'in the first quarter' attached to '11%' lets strict reader confirm; qualifiers were the good half of exp13 |
| 15 | Labeled logistics rows (Date:/Duration:/Team size:/Founded:/Trial:) | 89.6% (43/48) | +2.1 | KEEP | Event page 8/8; labeled rows beat extra question-headings — retrieval anchors without collisions |
