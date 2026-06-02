# M142 Cyclist Model — UCLA Math 142 Group Project

Group modeling project for **UCLA Math 142** (COMAP-style). Our chosen problem models a **cyclist's performance** — how a rider's power output translates into speed and time over a course under aerodynamic drag, rolling resistance, and gravity on a gradient. The model code lives in [`src/`](src/); the written solution lives in Overleaf (linked below).

> **Assignment:** see [`docs/assignment/`](docs/assignment/). Deliverables: a 10–20 page paper, a presentation (≤20 min), peer evaluations, and two professor/TA consultations.
>
> 🚀 **New to the team or to git? Start with [`START-HERE.md`](START-HERE.md)** — 10-minute setup, no command line needed.

## Repository layout

| Path | What's in it |
|------|--------------|
| [`src/`](src/) | The model code — see [The model](#the-model) below. |
| [`notebooks/model_v2_simple_power.ipynb`](notebooks/model_v2_simple_power.ipynb) | Early prototype (time-stepping). Superseded by `src/`; kept as proof of work. |
| [`notebooks/archive/`](notebooks/archive/) | Earlier versions, kept as revision history / proof of work. |
| [`references/`](references/) | Source materials (papers, constants). |
| [`docs/assignment/`](docs/assignment/) | The official assignment instructions. |
| [`docs/problem.md`](docs/problem.md) | The problem (2022 MCM A) and a requirements checklist. |
| [`docs/paper-outline.md`](docs/paper-outline.md) | Rubric-aligned section skeleton for the write-up. |
| [`docs/proof-of-work/`](docs/proof-of-work/) | Photos/scans of handwritten derivations, scratch work, meeting notes — bring these to consultations. |
| [`data/courses/`](data/courses/) | Course files (CSV of segments) the model reads. |
| [`data/`](data/) | Any other empirical data we add. |

## The model

The model takes a **course** (an ordered list of segments) and a **rider power**, and returns the speed and time for each segment plus the total race time.

For each segment $i$, the rider's power $P_i$ must overcome aerodynamic drag, rolling resistance, and gravity to hold a steady speed $v_i$:

$$P_i = v_i\left[\tfrac{1}{2}\,\rho\,C_dA\,(v_i + w_i)^2 + C_{rr}\,m\,g + m\,g\,\text{grade}_i\right]$$

We know the rider's power and solve this for $v_i$ — there is no closed form (it is cubic in $v_i$), so `physics.py` finds it numerically. The segment time is distance over speed plus a turn penalty $\tau_i$, and the race time is the sum over segments:

$$T_i = \frac{d_i}{v_i} + \tau_i \qquad\qquad T_\text{total} = \sum_i T_i$$

Symbols: $\rho$ air density, $C_dA$ drag area, $C_{rr}$ rolling-resistance coefficient, $m$ rider + bike mass, $g$ gravity, $w_i$ segment headwind, $\text{grade}_i$ slope as a fraction, $d_i$ segment distance, $\tau_i$ turn penalty.

**Rider model and pacing.** Each rider is a *critical-power* model: a sustainable power $\text{CP}$ plus a finite anaerobic reserve $W'$ (joules). Riding above CP drains the reserve at rate $P-\text{CP}$; riding below refills it; it can never go negative — that single rule is the rider's energy/fatigue limit. The model compares two strategies: holding CP the whole way (never spending the reserve) versus spending $W'$ on the climbs, where it buys the most time. The gap between them is the value of pacing.

| File | Role |
|------|------|
| [`src/parameters.py`](src/parameters.py) | Physics constants and rider profiles. |
| [`src/course.py`](src/course.py) | Loads a course CSV into segments. |
| [`src/physics.py`](src/physics.py) | Solves speed from power for one segment. |
| [`src/pacing.py`](src/pacing.py) | Critical-power reserve (W′) accounting and pacing strategies. |
| [`src/simulate.py`](src/simulate.py) | Runs constant-CP vs. paced riding and reports the time saved. |

Run it:

```bash
python src/simulate.py
```

## Course parameters

A course is an ordered list of **segments**, stored as a CSV in [`data/courses/`](data/courses/). Each segment carries the four things the model needs:

| Field | Symbol | Meaning |
|-------|--------|---------|
| `distance_m` | $d_i$ | Segment length, metres. |
| `grade_pct` | $\text{grade}_i$ | Average slope in percent (+ up / − down). |
| `turn_penalty_s` | $\tau_i$ | Time lost braking/cornering, seconds (0 if none). |
| `wind_exposure` | $w_i$ | `low` / `medium` / `high`, mapped to an effective headwind in [`src/parameters.py`](src/parameters.py). |

The three courses the problem requires:

| File | Course | Status |
|------|--------|--------|
| `custom_5km_loop.csv` | Self-designed loop — 4 turns, a climb + descent, returns to start. | Ready (worked example). |
| `tokyo_olympic_tt.csv` | 2021 Olympic ITT, Tokyo. | Template — to parameterise. |
| `flanders_world_tt.csv` | 2021 UCI Worlds ITT, Flanders. | Template — to parameterise. |

To parameterise a real course: split the route into segments, then for each give its distance, average grade, a turn penalty wherever the rider must brake, and a wind-exposure label. The wind labels map to headwind speeds in [`src/parameters.py`](src/parameters.py) — tune those as a group. Column details: [`data/courses/README.md`](data/courses/README.md).

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

# run the model (uses only the Python standard library)
python src/simulate.py
```

The early prototype notebook is optional and needs `pip install numpy matplotlib jupyter` to open.
