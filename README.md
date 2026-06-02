# M142 Cyclist Model — UCLA Math 142 Group Project

Group modeling project for **UCLA Math 142** (COMAP-style). Our chosen problem models a **cyclist's performance** — how a rider's power output translates into speed and distance over a course under forces such as aerodynamic drag, gravity on a gradient, and rider fatigue. The model code lives in [`src/`](src/); the written solution lives in Overleaf (linked below).

> **Assignment:** see [`docs/assignment/`](docs/assignment/). Deliverables: a 10–20 page paper, a presentation (≤20 min), peer evaluations, and two professor/TA consultations.
>
> 🚀 **New to the team or to git? Start with [`START-HERE.md`](START-HERE.md)** — 10-minute setup, no command line needed.

## Repository layout

| Path | What's in it |
|------|--------------|
| [`src/`](src/) | The model code — see [The model](#the-model) below. |
| [`notebooks/model_v2_simple_power.ipynb`](notebooks/model_v2_simple_power.ipynb) | Early prototype — an exploratory time-stepping version. |
| [`notebooks/archive/`](notebooks/archive/) | Earlier versions, kept as revision history / proof of work. |
| [`references/`](references/) | Source materials (papers, constants). |
| [`docs/assignment/`](docs/assignment/) | The official assignment instructions. |
| [`docs/paper-outline.md`](docs/paper-outline.md) | Rubric-aligned section skeleton for the write-up. |
| [`docs/proof-of-work/`](docs/proof-of-work/) | Photos/scans of handwritten derivations, scratch work, meeting notes — bring these to consultations. |
| [`data/courses/`](data/courses/) | Course files (CSV of segments) the model reads. |
| [`data/`](data/) | Any other empirical data we add. |

## The model

The model takes a **course** (an ordered list of segments) and a **rider power**, and returns the speed and time for each segment plus the total race time.

For each segment it solves a steady-state power balance for the speed `v`:

```
P = v * ( 0.5*rho*CdA*(v + wind)^2   # aerodynamic drag
          + Crr*m*g                  # rolling resistance
          + m*g*grade )              # gravity along the slope
```

then adds any turn penalty — `time = distance / v + turn_penalty` — and sums over segments for the total time.

| File | Role |
|------|------|
| [`src/parameters.py`](src/parameters.py) | Physics constants and rider profiles. |
| [`src/course.py`](src/course.py) | Loads a course CSV into segments. |
| [`src/physics.py`](src/physics.py) | Solves speed from power for one segment. |
| [`src/simulate.py`](src/simulate.py) | Runs one rider over one course and prints segment times. |

Run it:

```bash
python src/simulate.py
```

Course files live in [`data/courses/`](data/courses/) — see the README there for the format.

## Links

- 📝 **Paper (Overleaf):** <!-- paste the Overleaf share link here -->
- 📋 **Project sign-up sheet:** https://docs.google.com/spreadsheets/d/1zr8BNPS1wVuw7ZPD5pIbW7FvJqMs6sMdaK7anrhqdo/edit
- 🤝 **How to contribute:** [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Team

| Name | GitHub | Focus |
|------|--------|-------|
| Carter Dandridge | @wochaotom | Course Parameters |
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
