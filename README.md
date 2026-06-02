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

**Rider model and pacing.** Each rider is a *critical-power* model: a sustainable power $\text{CP}$ plus a finite anaerobic reserve $W'$ (joules). Riding above CP drains the reserve at rate $P-\text{CP}$; riding below refills it; it can never go negative — that single rule is the rider's energy/fatigue limit. The model compares two strategies: holding CP the whole way (never spending the reserve) versus spending $W'$ on the slowest sections (climbs and headwinds), where it buys the most time. The gap between them is the value of pacing.

| File | Role |
|------|------|
| [`src/parameters.py`](src/parameters.py) | Physics constants and rider profiles. |
| [`src/course.py`](src/course.py) | Loads a course CSV into segments. |
| [`src/physics.py`](src/physics.py) | Solves speed from power for one segment. |
| [`src/pacing.py`](src/pacing.py) | Critical-power reserve (W′) accounting and pacing strategies. |
| [`src/simulate.py`](src/simulate.py) | Runs constant-CP vs. paced riding and reports the time saved. |
| [`src/sensitivity.py`](src/sensitivity.py) | Wind and power-deviation sensitivity analyses. |
| [`src/compare.py`](src/compare.py) | Rider × course matchup — every rider across every course. |

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

| File | Course | Distance | Climbing | Sharp turns | Status |
|------|--------|---------:|---------:|:-----------:|--------|
| `custom_5km_loop.csv` | Self-designed **technical loop** | 5.0 km | one 6% ramp | 4 | Ready |
| `tokyo_olympic_tt.csv` | Tokyo 2021 Olympic ITT (1 lap; men ride 2) | 22.1 km | ~423 m | speedway + 2 climbs | Gradients sourced, lengths inferred |
| `flanders_world_tt.csv` | Flanders 2021 Worlds ITT (men) | 43.3 km | ~78 m (flat) | seafront / Damme / Bruges | Confirmed flat |

Tokyo's climb gradients are quoted from race previews; its segment lengths and descents, plus all wind-exposure labels, are estimates — provenance in [`data/courses/README.md`](data/courses/README.md) and [`references/data-sources.md`](references/data-sources.md). To add or refine a course: split the route into ordered segments, and give each a distance, average grade, a turn penalty where the rider brakes, and a wind label.

## Results so far

> Current model output — reproduce with the scripts in `src/`. Tokyo's gradients and the rider/wind parameters are estimates within sourced ranges, so treat the **magnitudes** as provisional; the **patterns** are the findings.

**Pacing beats flat power.** Custom loop, male TT specialist: riding constant critical power = **440.9 s**; spending the $W'$ reserve on the slow sections = **405.8 s** → **~35 s (8%) saved**. (`simulate.py`)

**Wind dominates — and a plan can break.** One plan held into different winds (`sensitivity.py`): a **±4 m/s** shift moves the finish **−58 s to +78 s** (−14% to +19%). Into a headwind the planned reserve-spend goes infeasible — the climbs take longer and drain $W'$ to empty.

**Execution error is asymmetric.** The optimal plan already empties $W'$, so the rider can underperform (−5% power → +9 s) but cannot *sustainably* overperform (going harder runs the reserve negative). A realistic ±5% miss ≈ ±2% on the finish.

**Rider × course cross-over (headline).** Climber minus TT-specialist finishing time (negative = climber faster):

| | custom | Tokyo (hilly) | Flanders (flat) |
|--|---:|---:|---:|
| **male** | +8.5 s | **−21.6 s** | +56.8 s |
| female | +14.9 s | +6.8 s | +174.0 s |

The **male climber wins hilly Tokyo** but loses the flatter courses — the terrain-dependent advantage the problem is built around, matching the real races (climbers/all-rounders won Tokyo, TT engines won Flanders). The **female gap narrows on Tokyo (+6.8 s) but does not invert** even with realism-corrected parameters (a heavier, more powerful female TT specialist; a lighter climber). We do **not** force it: the real female Tokyo winner (van Vleuten) was an exceptional all-rounder, not a representative light climber, so a clean *type-level* female cross-over isn't expected — a model-assessment finding, not a fault. (`compare.py`)

**Validation vs the 2021 winners.** With an elite-but-not-champion archetype (CP 350 W), the model runs **~12–27% slower** than the actual winners (Flanders: 3439 s model vs 2868 s for Ganna). The physics is the right shape; the gap is the archetype CP sitting well below a world-champion's (~490 W). Right model, calibratable inputs.

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
