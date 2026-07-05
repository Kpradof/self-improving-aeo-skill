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
| 16 | Entity named at most once in intro | 81.2% (39/48) | -8.4 | REVERT | Directionally right on page 01 but rewriter reshuffles whole pages; single-sample variance dominates small negative-space rules |
| 17 | Key-facts table immediately after H1 | 85.4% (41/48) | -4.2 | REVERT | Duplicating facts up top splits retrieval between summary and section chunks; page 06 lost narrative context rows |
| 18 | Rigid page skeleton (H1 → 1-line intro → fact sections → narrative last) | 85.4% (41/48) | -4.2 | REVERT | Templating didn't tame variance; pushing narrative last hurts story pages (03: 5/8) whose questions live in the narrative |
| 19 | Labeled stat lines inline within narrative | 87.5% (42/48) | -2.1 | REVERT | Close (page 03 recovered 7/8) but page 04 wobbled 8→6; within noise band of best, not above it |
| 20 | Dedicated 'Results' section with labeled metric rows | 85.4% (41/48) | -4.2 | REVERT | Duplicating metrics into a Results section splits retrieval mass again — same failure family as exp04/exp17 (duplication ≠ coverage) |
| 21 | Entity name mandatory in every heading | 85.4% (41/48) | -4.2 | REVERT | Entity in every heading makes headings interchangeable for retrieval (all share brand token); differentiation comes from topic words |
| 22 | Sections under ~100 words (one quotable unit each) | 87.5% (42/48) | -2.1 | REVERT | Within noise of best; splitting topics into two headings dilutes the winning single-anchor pattern |
| 23 | Search-term synonyms in parentheses at the fact | 87.5% (42/48) | -2.1 | REVERT | Again 42/48 — three straight experiments land exactly here; best (43/48) may be a lucky sample of the same rule set |
| 24 | Interaction: inline stat lines + parenthetical synonyms | 81.2% (39/48) | -8.4 | REVERT | Combo hurt — extra annotations everywhere flatten keyword contrast between sections. Rules interact through the retrieval budget |
| 25 | Rewriter self-check: every likely question → exactly one winning section | 91.7% (44/48) | +2.1 | KEEP | Process rule beats structure rules: pushing retrieval-disambiguation INTO the rewriter fixed both narrative pages (03, 06: 8/8) |
| 26 | Extend labeled rows: support/services/locations | 87.5% (42/48) | -4.2 | REVERT | Fixed the targeted questions (02, 05 up) but narrative pages regressed — longer label lists crowd out the self-check rule's judgment |
| 27 | Anti-tie clause: strip question words from non-answering sections | 81.2% (39/48) | -10.5 | REVERT | Over-aggressive: rewriter stripped legit keywords from fact sections too; 'remove words' instructions are dangerous |
| 28 | Positive anti-tie: strengthen the answering section only | 89.6% (43/48) | -2.1 | REVERT | Better than exp27's stripping but still under champion; self-check as-is already handles most ties |
| 29 | Active voice, subject-verb-object sentences | 87.5% (42/48) | -4.2 | REVERT | Style-level rules don't move a retrieval-dominated metric; extraction already works once the right chunk is found |
| 30 | Simplification: delete 'clear prose' rule | 87.5% (42/48) | -4.2 | REVERT | Even a bland rule contributes; removal isn't free |
| 31 | Intro = one definitional sentence only | 89.6% (43/48) | -2.1 | REVERT | Three pages at 8/8 but page 02 collapsed to 5/8 (agency page needs its founding-story context); close but under champion |
| 32 | Person + role + affiliation in one sentence | 85.4% (41/48) | -6.3 | REVERT | People questions weren't failing; rule spent rewriter attention where there was nothing to win |
| 33 | Self-check via explicit search simulation over ~100-word passages | 81.2% (39/48) | -10.5 | REVERT | Rewriting the champion's best rule made it worse — 'exactly one section' phrasing was load-bearing; don't paraphrase winners |
| 34 | One topic per section, never fold two themes under one heading | 93.8% (45/48) | +2.1 | KEEP | Topic purity maximizes keyword contrast BETWEEN sections — the structural complement of the self-check rule |
| 35 | Echo topic noun in heading + first row | 79.2% (38/48) | -14.6 | REVERT | Same family as exp09: any 'repeat keywords' rule degrades global contrast. Density rules are dead — structure + self-check is the winning formula |
| 36 | Delete closing CTAs, rescue their facts first | 87.5% (42/48) | -6.3 | REVERT | Page 02 perfect but 03 sank; rewriter treats 'delete' rules as license to compress narratives too |
| 37 | Numbered steps opening with timing/trigger | 85.4% (41/48) | -8.4 | REVERT | Targeted one failing question, cost more elsewhere; the champion is now hard to beat with narrow rules |
