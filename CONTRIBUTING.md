# Contributing

A short guide so we collaborate cleanly and leave a clear trail of who did what — which doubles as **proof of work** for the consultations.

## Golden rules

1. **Commit from your own GitHub account.** Commits are attributed to their author; that attribution is the evidence the work was genuinely shared across the group.
2. **Commit early and often.** Small, frequent commits with clear messages tell the story of how the model evolved. A perfect model with no history gets scrutinized.
3. **Never commit AI-generated math, analysis, or paper prose.** See the AI policy in the [README](README.md). Log any *allowed* AI help in [`docs/AI-USE-LOG.md`](docs/AI-USE-LOG.md).

## Workflow (pull requests)

We use a light pull-request workflow so changes get a second pair of eyes:

```bash
# start from an up-to-date main
git checkout main && git pull

# make a branch for your piece of work:  <yourname>/<short-topic>
git checkout -b carter/fatigue-tuning

# work, then commit
git add -A
git commit -m "Tune fatigue recovery rate and note the reasoning"

# push and open a pull request
git push -u origin carter/fatigue-tuning
gh pr create          # or open the PR link GitHub prints
```

A teammate reviews and merges into `main`. For tiny fixes (a README typo, say) committing straight to `main` is fine.

## Python environment

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate      macOS/Linux:  source .venv/bin/activate
pip install numpy matplotlib jupyter
```

## Working with notebooks

Notebooks are stored as JSON, outputs included, so they can produce noisy diffs and the occasional merge conflict.

- Try to have **one person own a given notebook** at a time.
- The current working notebook is [`notebooks/model_v2_simple_power.ipynb`](notebooks/model_v2_simple_power.ipynb). Older versions live in [`notebooks/archive/`](notebooks/archive/) — **don't delete them**, they're our history.
- If conflicts get annoying, we'll add [`nbstripout`](https://github.com/kynan/nbstripout) to strip outputs before commit:
  ```bash
  pip install nbstripout && nbstripout --install
  ```

## Proof of work

Drop photos/scans of handwritten derivations, scratch notes, and meeting notes into [`docs/proof-of-work/`](docs/proof-of-work/), named by date (e.g. `2026-06-03-fatigue-derivation.jpg`). Bring them to the consultations.
