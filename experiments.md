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
| 38 | Plain H1: entity + category, no taglines | 89.6% (43/48) | -4.2 | REVERT | Title words rarely collide with questions; taglines were harmless |
| 39 | Evict section-owned facts from the intro | 85.4% (41/48) | -8.4 | REVERT | Third intro-family failure (16, 31, 39): every intro constraint destabilizes the rewriter more than it fixes retrieval |
| 40 | Mission reframe: passage-retrieval mechanics in preamble | 85.4% (41/48) | -8.4 | REVERT | Explaining the mechanism made the rewriter over-engineer pages; concrete rules beat conceptual framing |
| 41 | Bullet sentences instead of pipe tables | 83.3% (40/48) | -10.5 | REVERT | Format micro-management underperforms letting the rewriter choose per page |
| 42 | Digits with attached units, never spelled out | 83.3% (40/48) | -10.5 | REVERT | Gold answers use original phrasing; converting 'four hours' to '4 hours' can even hurt judge matching. Formatting rules keep losing |
| 43 | Rule order: self-check moved to position 1 | 91.7% (44/48) | -2.1 | REVERT | Order matters little; check-last placement (recency) at least ties check-first |
| 44 | Sections ordered by search likelihood | 89.6% (43/48) | -4.2 | REVERT | Position within page doesn't matter to per-question retrieval; reordering just reshuffles the noise |
| 45 | Label every fact with its question's noun phrase | 85.4% (41/48) | -8.4 | REVERT | Universal labeling turns pages into glossaries and degrades narrative pages; scoped labels (exp15) were the right dose |
| 46-48 | Variance check: 3 fresh rewrite samples of the champion ruleset | 75.0% / 83.3% / 79.2% | — | MEASURE | THE run's biggest finding: champion's 93.8% was a lucky sample. True champion mean ≈ 82.8% (n=4, σ≈7 pts). Single-sample keep/revert gating is unreliable — next run must gate on mean-of-3 |
| 49-50 | Mean of simple 5-rule set (exp02 era): 3 samples | 83.3% / 75.0% / 79.2% | — | MEASURE | Simple-set mean 79.2% vs champion mean 82.8%: the 4 extra rules buy ~+3.6 pts on average — real but modest; most of the lift (66.7→~80) comes from the first two structural rules |

## Run 1 summary (2026-07-05, 50 experiments, Opus 4.8 rewriter)

**Scores** (QA accuracy under simulated answer-engine retrieval):
- Dev baseline (original pages): 66.7%
- Champion ruleset, best sample: 93.8% · mean of 4 samples: 82.8% (σ ≈ 7 pts)
- Holdout baseline: 62.5% → champion on holdout: **83.3% (+20.8 pts)** — rules generalize; no overfitting.

**Rules that survived (the champion, 9 rules):** self-contained sentences with explicit entities (exp01) · question-shaped headings (exp02) · one complete fact per row with qualifiers attached (exp10+14) · labeled logistics rows (exp15) · rewriter self-check "every question → exactly one winning section" (exp25) · one topic per section (exp34).

**What died, by family:**
- Duplication (FAQ, key-facts box, Results section): splits retrieval mass — coverage ≠ copies (exp04, 17, 20).
- Keyword density/stacking anywhere: destroys contrast BETWEEN sections (exp09, 11, 24, 35).
- Intro constraints (minimal, definitional, fact-eviction): destabilize the rewriter more than they fix retrieval (exp08, 16, 31, 39).
- Formatting micro-management (active voice, digits, bullets-vs-tables, plain H1): style doesn't move a retrieval-dominated metric (exp29, 38, 41, 42).

**Method finding (the big one):** rewrite sampling variance (~±7-9 pts) exceeds most single-rule effects. The 93.8% best sample was luck; several REVERTed rules may have been real improvements lost to noise. **Next run: gate keep/revert on the mean of 3 rewrite samples**, not one.

**Ideas for run 2:** mean-of-3 gating · per-page-type rule branches (product vs narrative) · larger dev set to cut eval noise · test rules against embedding-based retrieval, not just lexical.

## Run 2 setup (2026-07-05) — real pages

Corpus: 14 real scraped pages (9 dev / 5 holdout), 112 agent-generated questions, stratified (pricing, landing, blog/guide). Pages in `data-real/` (gitignored — copyright); sources logged per page in `source.txt`. Protocol: `program2.md` (mean-of-3 gating, dual retrieval, plan-subagent rewrites).

**Baselines (dev, original pages):**
- Lexical retrieval: **56.9%** (41/72)
- Embedding retrieval (MiniLM): **40.3%** (29/72)

Run 1's synthetic corpus overstated page quality (66.7% baseline); real pages are messier and semantic retrieval is much harder. Headroom is large. Experiments start next session.

## Run 2 experiments (2026-07-06)

### exp2.01 — Transfer test: run-1 champion rules on real pages
- **Hypothesis:** the 9 champion rules from run 1 (structure + self-check) generalize from synthetic to real scraped pages.
- **Change:** none — SKILL.md as inherited from run 1. This experiment establishes the run-2 champion means.
- **Samples (dev, 9 pages × 8 Q):**
  | Sample | Lexical | Embedding |
  |---|---|---|
  | s1 | 70.8% (51/72) | 59.7% (43/72) |
  | s2 | 66.7% (48/72) | 66.7% (48/72) |
  | s3 | 66.7% (48/72) | 62.5% (45/72) |
  | **Mean** | **68.1%** | **63.0%** |
- **Baselines (original pages):** lexical 56.9%, embedding 40.3%.
- **Verdict: KEEP (champion established).** +11.2 pts lexical, +22.7 pts embedding over originals. The rules transfer; the gain is larger under embedding retrieval than lexical — self-contained sentences and question-shaped headings help semantic matching even more than keyword matching.
- **Notes:** rewrites via Sonnet plan-subagents (hybrid plan B). Wave-1 samples for pages 06/07 exceeded the ±30% length rule (+120%/+75%) before the prompt was tightened; later samples comply. Weak pages across all samples: page-04 (mailchimp, huge table-heavy page: 1-5/8 lexical) and page-09 (tailscale, 4.4k words: 2-3/8) — long pages chunk into many sections and retrieval misses. Batched multi-page subagents cut plan-token cost ~4× vs one subagent per page.

### exp2.02 — Per-plan sections instead of one big comparison table
- **Hypothesis:** on multi-plan pages, plan facts buried in one large comparison table fail retrieval — 120-word chunking separates the header row (plan names) from value rows, and every chunk mentions all plan names, so lexical overlap ties and misses. Offline diagnosis of exp2.01 s3: gold-answer coverage of the retrieved chunk was 0.00–0.33 for most page-04/page-09 questions.
- **Change:** new rule 9 — each plan/tier gets its own section with a question-phrased heading naming the plan; every fact about the plan lives inside its section, each row naming the plan; never present plan facts only in one comparison table spanning plans.
- **Samples (dev):**
  | Sample | Lexical | Embedding |
  |---|---|---|
  | s1 | 79.2% (57/72) | 66.7% (48/72) |
  | s2 | 72.2% (52/72) | 68.1% (49/72) |
  | s3 | 75.0% (54/72) | 69.4% (50/72) |
  | **Mean** | **75.5%** | **68.1%** |
- **Champion means:** lexical 68.1%, embedding 63.0%.
- **Verdict: KEEP.** +7.4 lexical, +5.1 embedding — beats champion in both modes; first run-2 rule accepted under mean-of-3 dual gating. New champion means: lexical 75.5%, embedding 68.1%.
- **Insight:** the run-1 "tables win" finding inverts on real pages — tables help only when they are small and single-topic. Cross-plan comparison tables are a retrieval hazard: chunking destroys row–header adjacency. Restructuring to per-plan sections is the single biggest real-page gain so far.
