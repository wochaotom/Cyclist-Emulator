# Start here

Onboarding for the team — **no git experience needed.** About 10 minutes.

## 1. Get added to the repo
Make a free account at [github.com](https://github.com), then send your **username** to Carter (`@wochaotom`). You'll get an email invite — click **Accept**.

## 2. Install GitHub Desktop
Download from **https://desktop.github.com** and install it. Open it and **sign in with your GitHub account.** This also sets your identity automatically, so your work is credited to you — nothing to configure.

## 3. Clone the project to your computer
In GitHub Desktop: **File → Clone repository → GitHub.com tab → pick `Cyclist-Emulator` → choose a folder → Clone.** The project files are now on your computer.

## 4. (Optional) Run the model
The model is plain Python — standard library only, nothing to install. In a terminal:
```
python src/simulate.py
```
The old prototype notebooks in `notebooks/archive/` need `pip install numpy matplotlib jupyter` to open, but you don't need them for the model or the write-up.

## The daily routine (this is the whole workflow)
Every time you sit down to work, in GitHub Desktop:
1. **Fetch origin** (top bar) — pulls in everyone's latest work. **Always do this first.**
2. Edit files / the notebook / the paper.
3. Bottom-left: type a short **Summary** of what you changed, then **Commit to main**.
4. **Push origin** (top bar) — uploads your work so the team has it.

That's it: **Fetch → work → Commit → Push.** Commit and push often — anything you've **pushed is safely backed up**; anything you haven't isn't.

## The one rule that prevents headaches
**Don't edit the same notebook as someone else at the same time.** Jupyter notebooks clash badly when two people change them at once. Just say *"I've got the model notebook this afternoon"* in the group chat before you start.

## Where things live
- `src/` — the model code (`python src/simulate.py` runs it)
- `data/courses/` — the course files
- `docs/` — paper outline, the assignment, and proof-of-work (derivation photos, meeting notes)
- `references/` — source papers and constants
- `notebooks/archive/` — earlier prototypes (proof of work)

Stuck? Ask in the group chat — someone's probably hit the same thing.
