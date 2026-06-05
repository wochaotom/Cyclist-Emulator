# Cyclist-Emulator

UCLA Math 142 group project for 2022 MCM Problem A (power profile of a cyclist): given a rider's sustainable power and fatigue limits, find how to distribute power over a time-trial course to minimize finishing time.

## Repository layout

| Path | Contents |
|------|----------|
| `notebooks/model_v3.ipynb` | The model: time-stepping simulation with power-threshold fatigue. |
| `data/courses/` | Course files (CSV, one row per segment) — the course parameters. |
| `data/real_results.csv` | 2021 ITT finishing times used as validation targets. |
| `references/data-sources.md` | Sources for course geometry, race results, and physical/physiological parameters. |
| `references/references.md` | Deduplicated citation list. |
| `docs/problem.md` | Problem statement (2022 MCM A) and requirements checklist. |
| `docs/assignment/` | Official assignment instructions. |
| `docs/proof-of-work/` | Handwritten derivations, scratch work, meeting notes. |
| `archive/` | Earlier prototypes (v1, v2) and the retired CP/W′ model. |
| `paper/` | LaTeX scaffold. |

## Model

`notebooks/model_v3.ipynb`. The rider and bike are treated as one mass. Each time step sets a target power from the segment gradient, caps it at a fatigue-reduced ceiling, subtracts aerodynamic drag, gravity, and rolling resistance to get net force, and integrates speed and distance forward (Euler, 1-second steps). Fatigue accumulates while power is above a threshold and recovers below it. Parameter values and the derivation are in the team write-up.

`archive/cp_w_prime_model/` holds an earlier critical-power (CP/W′) model, kept as the alternative modeling choice discussed in the paper.

## Courses

A course is an ordered list of segments in a CSV under `data/courses/`. Columns:

| Column | Meaning |
|--------|---------|
| `segment_id` | Order index. |
| `name` | Segment label. |
| `distance_m` | Segment length, metres. |
| `grade_pct` | Average gradient, percent (+ uphill / − downhill). |
| `turn_penalty_s` | Time added for braking/cornering, seconds. |
| `wind_exposure` | `low` / `medium` / `high`, mapped to an effective headwind in the model. |

| File | Course | Distance | Climbing | Gradient source |
|------|--------|---------:|---------:|-----------------|
| `custom_5km_loop.csv` | Self-designed technical loop (4 sharp turns) | 5.0 km | one 6% ramp | self-designed |
| `tokyo_olympic_tt.csv` | Tokyo 2021 Olympic ITT (1 lap; men ride 2) | 22.1 km | ~390 m | NBC elevation breakdown |
| `flanders_world_tt.csv` | Flanders 2021 Worlds ITT (men) | 43.3 km | ~78 m (flat) | UCI technical guide |

Distance and gradient are sourced; turn penalty and wind label are modeling assignments. Per-field provenance is in `data/courses/README.md` and `references/data-sources.md`.

## Status

The model and the three course files are in place. Remaining work: run the model on the three courses, run the wind and power-deviation sensitivity analyses and the rider-type comparison, and write the results, model assessment, and conclusion into the paper. Result tables and figures still in `paper/` came from the retired CP/W′ model and do not carry over.

## Running the model

```
git clone https://github.com/wochaotom/Cyclist-Emulator.git
cd Cyclist-Emulator
pip install numpy matplotlib jupyter
jupyter notebook notebooks/model_v3.ipynb
```

Select the course at the top of the course cell: `course_file = "tokyo_olympic_tt.csv"` (or `flanders_world_tt.csv`, `custom_5km_loop.csv`).

## Team

| Name | GitHub | Area |
|------|--------|------|
| Carter Dandridge | @wochaotom | Course parameters |
| Ben Miller | @benmiller74 | Rider model & parameters |

Workflow: `CONTRIBUTING.md`. First-time git setup: `START-HERE.md`.
