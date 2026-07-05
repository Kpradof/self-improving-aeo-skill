# Experiment Program

You are an autonomous research agent improving `SKILL.md` — a set of AEO (Answer Engine Optimization) rewrite rules. Your metric is QA accuracy: a small model reads each rewritten page and answers factual questions; the score is the fraction it gets right.

## The loop

Repeat until told to stop (or for the number of experiments requested):

1. **Read the log.** Open `experiments.md`. Never repeat a hypothesis that already failed. Build on what worked.
2. **Form ONE hypothesis.** A single, specific idea about what makes pages more answer-extractable. Examples of the *kind* of thing to explore: answer placement, heading structure, sentence subject clarity, entity naming, lists vs prose, redundancy of key facts, tables, question-shaped headings. One change per experiment — never bundle.
3. **Mutate `SKILL.md` only.** Add, edit, or remove rules to express the hypothesis.
4. **Run:**
   ```bash
   python3 rewrite.py --set dev
   python3 eval.py --set dev --source rewritten
   ```
5. **Decide.**
   - Score > best recorded score → keep: `git add SKILL.md experiments.md && git commit -m "expNN: <hypothesis> (+X.X pts)"`
   - Score ≤ best → revert: `git checkout -- SKILL.md` (but still log the result first)
6. **Log.** Append one row to the table in `experiments.md`: experiment number, hypothesis (one line), score, delta vs best, verdict (KEEP/REVERT), and one insight.
7. Go to 1.

Before the first experiment of a run, if `experiments.md` has no baseline row, record one: `python3 eval.py --set dev --source original` (score of the unrewritten pages) and `python3 rewrite.py --set dev && python3 eval.py --set dev --source rewritten` (score of the current SKILL.md).

## Hard constraints — violating any of these invalidates the run

- **Mutable file: `SKILL.md`. Nothing else.** Never edit `eval.py`, `rewrite.py`, `program.md`, this repo's data, or any file under `data/`.
- **Never read anything under `data/holdout/`.** Not the pages, not the questions. It exists to detect overfitting after the run ends. Reading it contaminates the experiment.
- You MAY read `data/dev/` pages and questions to form hypotheses, but `SKILL.md` must contain only **general rules**. It must never mention a specific dev page, question, answer, company name, or number from the dataset. A rule like "include an FAQ answering what Taskloom costs" is cheating; "state the price in the first paragraph of a pricing page" is a rule.
- Rules must never instruct the rewriter to invent, pad, or fabricate content.
- Do not touch git history (no rebase, no amend of old commits).

## End of run

1. Run the holdout check ONCE: `python3 rewrite.py --set holdout && python3 eval.py --set holdout --source rewritten`
2. Append a final summary section to `experiments.md`: best dev score vs baseline, holdout score vs holdout baseline (`eval.py --set holdout --source original`), overfitting verdict, top 3 rules discovered, and ideas for the next run.
3. Commit the log.
