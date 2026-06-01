# M142 Cyclist Model — UCLA Math 142 Group Project

Group modeling project for **UCLA Math 142** (COMAP-style). Our chosen problem models a **cyclist's performance** — how a rider's power output translates into speed and distance over a course under forces such as aerodynamic drag, gravity on a gradient, and rider fatigue. The mathematical work lives in the notebooks; the written solution lives in Overleaf (linked below).

> **Assignment:** see [`docs/assignment/`](docs/assignment/). Deliverables: a 10–20 page paper, a presentation (≤20 min), peer evaluations, and two professor/TA consultations.

## Repository layout

| Path | What's in it |
|------|--------------|
| [`notebooks/model_v2_simple_power.ipynb`](notebooks/model_v2_simple_power.ipynb) | **Active model** (current working version). |
| [`notebooks/archive/`](notebooks/archive/) | Earlier versions, kept as revision history / proof of work. |
| [`references/`](references/) | Source materials (papers, constants). |
| [`docs/assignment/`](docs/assignment/) | The official assignment instructions. |
| [`docs/paper-outline.md`](docs/paper-outline.md) | Rubric-aligned section skeleton for the write-up. |
| [`docs/AI-USE-LOG.md`](docs/AI-USE-LOG.md) | Running disclosure log of any AI assistance (required by the assignment). |
| [`docs/proof-of-work/`](docs/proof-of-work/) | Photos/scans of handwritten derivations, scratch work, meeting notes — bring these to consultations. |
| [`data/`](data/) | Any empirical or course data we add (elevation profiles, real power data, etc.). |

## Links

- 📝 **Paper (Overleaf):** <!-- paste the Overleaf share link here -->
- 📋 **Project sign-up sheet:** https://docs.google.com/spreadsheets/d/1zr8BNPS1wVuw7ZPD5pIbW7FvJqMs6sMdaK7anrhqdo/edit
- 🤝 **How to contribute:** [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Team

| Name | GitHub | Focus |
|------|--------|-------|
| Carter Dandridge | @wochaotom | |
| _add teammate_ | @_username_ | |

## Quickstart

```bash
git clone https://github.com/wochaotom/Cyclist-Emulator.git
cd Cyclist-Emulator

# (recommended) isolated Python environment
python -m venv .venv
# Windows:  .venv\Scripts\activate      macOS/Linux:  source .venv/bin/activate
pip install numpy matplotlib jupyter

jupyter notebook notebooks/model_v2_simple_power.ipynb
```

## AI-use policy (read before using any AI tool)

This assignment **caps the grade at 60% (plus possible academic-integrity review)** if AI is used to formulate the model, choose assumptions/variables/parameters, perform or interpret the analysis, or write paper content. AI is allowed only for grammar/formatting, plotting-code syntax you understand and verify, and background summaries you independently check. **All AI use must be logged in [`docs/AI-USE-LOG.md`](docs/AI-USE-LOG.md) and disclosed in the paper.** In Consultation 2, any member can be asked to defend any derivation.
