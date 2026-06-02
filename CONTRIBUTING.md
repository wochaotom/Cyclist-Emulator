# Contributing

A short guide so we collaborate cleanly and leave a clear trail of who did what — which doubles as **proof of work** for the consultations.

**New to git? Read [`START-HERE.md`](START-HERE.md) first** — it walks you through setup with GitHub Desktop, no command line needed.

## Golden rules

1. **Commit from your own GitHub account.** Commits are attributed to their author; that attribution is the evidence the work was genuinely shared across the group.
2. **Commit and push often.** Small, frequent commits tell the story of how the model evolved — and anything you've pushed is safely backed up. A perfect model with no history gets scrutinized.

## Workflow

Everyone works directly on `main` — the simplest thing that works for a one-week project. In GitHub Desktop the loop is:

1. **Fetch origin** — get everyone's latest work. **Always do this first.**
2. Make your changes.
3. **Commit to main** with a one-line summary.
4. **Push origin** when you stop.

Two habits keep it painless:
- **Fetch/pull before you start** (avoids upload clashes).
- **Don't edit the same notebook as someone else at the same time** — call it in the group chat first. `.ipynb` files conflict badly.

**Comfortable with git and want a safety net for a bigger change?** Optional — branch, push, open a PR:
```bash
git checkout -b yourname/topic
# ...make changes, commit...
git push -u origin yourname/topic   # then open the PR link GitHub prints
```
Direct-to-`main` is the default, though.

## Python environment (only if running the notebooks)

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate      macOS/Linux:  source .venv/bin/activate
pip install numpy matplotlib jupyter
```

## Working with the code and notebooks

The model is plain Python in [`src/`](src/) — it diffs and merges cleanly, so just edit it normally and follow the loop above.

The notebooks in [`notebooks/archive/`](notebooks/archive/) are **frozen prototypes** kept as proof of work — don't edit or delete them. (Notebooks store JSON with their outputs, so they merge badly; that's part of why the live model moved to `.py` files.)

## Proof of work

Drop photos/scans of handwritten derivations, scratch notes, and meeting notes into [`docs/proof-of-work/`](docs/proof-of-work/), named by date (e.g. `2026-06-03-fatigue-derivation.jpg`). Bring them to the consultations.
