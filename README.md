# Cyclist-Emulator — UCLA Math 142 Group Project

Group modeling project for **UCLA Math 142**, answering **2022 MCM Problem A** (power profile of a cyclist): given a rider's power and fatigue limits, how should they distribute power over a time-trial course to finish fastest?

> **Assignment:** [`docs/assignment/`](docs/assignment/) · **Problem + requirements:** [`docs/problem.md`](docs/problem.md). The write-up lives in the team's shared document.
>
> 🚴 **Canonical model:** [`notebooks/model_v3.ipynb`](notebooks/model_v3.ipynb) — a dynamic, time-stepping model with a power-threshold fatigue mechanic.
>
> **New to the team or to git?** Start with [`START-HERE.md`](START-HERE.md).

## Repository layout

| Path | What's in it |
|------|--------------|
| [`notebooks/model_v3.ipynb`](notebooks/model_v3.ipynb) | **The model** — dynamic time-stepping + fatigue. |
| [`data/courses/`](data/courses/) | Course files (CSV of segments) — the course parameters. |
| [`references/data-sources.md`](references/data-sources.md) | Sources for course data, real results, and physical/physiological values. |
| [`docs/assignment/`](docs/assignment/) | The official assignment instructions. |
| [`docs/problem.md`](docs/problem.md) | The problem (2022 MCM A) and a requirements checklist. |
| [`docs/proof-of-work/`](docs/proof-of-work/) | Handwritten derivations, scratch work, meeting notes — bring to consultations. |
| [`archive/`](archive/) | Earlier prototypes (v1, v2) and the retired CP/W′ model (`cp_w_prime_model/`) — proof of work; the CP/W′ model is the paper's "alternative modeling choice." |
| [`paper/`](paper/) | LaTeX scaffold (its results came from the retired model — see the note there). |

## The model

The canonical model is the dynamic, time-stepping model in [`notebooks/model_v3.ipynb`](notebooks/model_v3.ipynb): the rider and bike are treated as one mass; each time step sets a target power from the gradient, caps it by a fatigue-reduced ceiling, subtracts aerodynamic drag, gravity, and rolling resistance, then integrates speed and distance forward. Fatigue builds above a power threshold and recovers below it. The derivation and parameter choices are written up in the team document.

An earlier **critical-power (CP/W′)** model is kept in [`archive/cp_w_prime_model/`](archive/cp_w_prime_model/) — a different fatigue framework, used as the alternative modeling choice the rubric asks us to discuss.

## Course parameters

A course is an ordered list of **segments**, stored as a CSV in [`data/courses/`](data/courses/). Each segment carries the four things the model needs:

| Field | Meaning |
|-------|---------|
| `distance_m` | Segment length, metres. |
| `grade_pct` | Average slope in percent (+ up / − down). |
| `turn_penalty_s` | Time lost braking/cornering, seconds (0 if none). |
| `wind_exposure` | `low` / `medium` / `high`, mapped to an effective headwind in the model. |

The three courses the problem requires:

| File | Course | Distance | Climbing | Status |
|------|--------|---------:|---------:|--------|
| `custom_5km_loop.csv` | Self-designed technical loop (4 sharp turns) | 5.0 km | one 6% ramp | Ready |
| `tokyo_olympic_tt.csv` | Tokyo 2021 Olympic ITT (1 lap; men ride 2) | 22.1 km | ~423 m | Gradients sourced, lengths inferred |
| `flanders_world_tt.csv` | Flanders 2021 Worlds ITT (men) | 43.3 km | ~78 m (flat) | Confirmed flat |

Tokyo's climb gradients are quoted from race previews; its segment lengths/descents and the wind labels are estimates — provenance in [`data/courses/README.md`](data/courses/README.md) and [`references/data-sources.md`](references/data-sources.md).

## Status — what's left

The model and course parameters exist. Still to do: **produce the results on the canonical model** — apply it to the three courses, run the required **wind** and **power-deviation** sensitivity analyses and the **rider-type comparison**, then write the summary, results, model assessment, and conclusion into the paper. Earlier result tables/figures in this repo came from the retired CP/W′ model and do not carry over directly.

## Links

- 📝 **Write-up:** <!-- paste the shared doc / Overleaf link here -->
- 📋 **Project sign-up sheet:** <!-- link -->
- 🤝 **How to contribute:** [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Team

| Name | GitHub | Focus |
|------|--------|-------|
| Carter Dandridge | @wochaotom | Course parameters |
| Ben Miller | @benmiller74 | Rider model & parameters |
| _add teammate_ | @_username_ | |

## Quickstart

```bash
git clone https://github.com/wochaotom/Cyclist-Emulator.git
cd Cyclist-Emulator
pip install numpy matplotlib jupyter
jupyter notebook notebooks/model_v3.ipynb
```
