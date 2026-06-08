# Cyclist-Emulator

UCLA Math 142 group project for 2022 MCM Problem A (power profile of a cyclist): given a rider's sustainable power and fatigue limits, find how to distribute power over a time-trial course to minimize finishing time.

## Repository layout

| Path | Contents |
|------|----------|
| `notebooks/model_v5.ipynb` | The model: time-stepping simulation + power-threshold fatigue, with scipy-optimized pacing. |
| `data/courses/` | Course files (CSV, one row per segment) — the course parameters. |
| `data/real_results.csv` | 2021 ITT finishing times used as validation targets. |
| `data/rider_profiles.csv` | Rider parameter sets (one row per profile) |
| `references/data-sources.md` | All sourced values and citations — course geometry, race results, physical/physiological parameters. |
| `results/` | Optimization sweep outputs — finishing-time table, per-segment power, and comparison plots. |
| `docs/assignment/` | Official assignment instructions. |
| `docs/proof-of-work/` | Handwritten derivations, scratch work, meeting notes. |
| `archive/` | Earlier prototypes (v1, v2), the retired CP/W′ model, and the archived LaTeX scaffold. |

## Model

`notebooks/model_v5.ipynb`. The rider and bike are treated as one point mass, pushed forward by the rider against air, road, and gravity, and stepped forward in time.

On a segment of slope angle $\theta = \arctan(\text{grade}\%/100)$, the resisting forces are aerodynamic drag, rolling resistance, and gravity:

$$F_\text{drag} = \tfrac{1}{2}\,\rho\,C_dA\,(v+w)^2, \quad F_\text{roll} = C_{rr}\,m\,g\cos\theta, \quad F_\text{grav} = m\,g\sin\theta$$

where $v$ is speed and $w$ the effective headwind from the segment's wind label. The rider's propulsive force is power divided by speed, $F_\text{rider} = P_\text{out}/\max(v,\,0.5)$ (the floor avoids dividing by zero at the start). Net force is integrated forward with a one-second step:

$$F_\text{net} = F_\text{rider} - F_\text{drag} - F_\text{roll} - F_\text{grav}, \qquad v \leftarrow \mathrm{clamp}\!\left(v + \tfrac{\Delta t}{m}F_\text{net},\ 0,\ v_\text{max}\right), \qquad x \leftarrow x + v\,\Delta t$$

Target power rises with gradient (harder uphill, easier down) and is capped by a fatigue-reduced ceiling:

$$P_\text{target} = \max(50,\ P_\text{base} + k_\text{hill}\,\theta), \qquad P_\text{out} = \min\!\big(P_\text{target},\ P_\text{max}(1 - c_\text{fat}\cdot\text{fat})\big)$$

Fatigue grows when output exceeds a threshold and recovers below it (clamped to $[0,1]$):

$$\Delta\text{fat} = r_\text{fat}\left(\frac{P_\text{out}-P_\text{thr}}{P_\text{thr}}\right)^2 \Delta t \quad \text{if } P_\text{out} > P_\text{thr}, \qquad \Delta\text{fat} = -r_\text{rec}\,\Delta t \quad \text{otherwise}$$

Each segment also adds its `turn_penalty_s` to the clock for cornering. Symbols map to code as $\rho$ = `a_density`, $C_dA$ = `CdA`, $C_{rr}$ = `Crr`, $k_\text{hill}$ = `hill_factor`, $P_\text{thr}$ = `P_threshold`, $c_\text{fat}$ = `fatigue_impact`, $r_\text{fat}$ = `fatigue_rate`, $r_\text{rec}$ = `recovery_rate`. Parameter values and their justification are in the team write-up.

Pacing is set by two knobs — `hill_factor` (extra power per unit gradient) and `flat_boost` (power held above `P_base` on flats and descents) — and `scipy.optimize.minimize` searches them for the time-minimizing strategy for each rider on each course. Tokyo is one lap; set `laps = 2` for the men's race.

`archive/cp_w_prime_model/` holds an earlier critical-power (CP/W′) model — a different fatigue framework, kept as the alternative modeling choice discussed in the paper.

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
| `tokyo_olympic_tt.csv` | Tokyo 2021 Olympic ITT (1 lap; men ride 2) | 22.1 km | ~310 m | 26-seg reconstruction, scaled to 22.1 km |
| `flanders_world_tt.csv` | Flanders 2021 Worlds ITT (men) | 43.3 km | ~78 m (flat) | UCI technical guide |

Distance and gradient are sourced; turn penalty and wind label are modeling assignments. Per-field provenance is in `data/courses/README.md` and `references/data-sources.md`.

## Rider profiles

Riders load the same way as courses — one row per profile in `data/rider_profiles.csv`, selected by `rider = "..."` in the notebook's Rider Parameters cell. `baseline` reproduces the originally submitted rider and is kept only as a calibration reference (the results comparison uses the four typed riders); the typed profiles are derived from the sourced ranges (power from W/kg figures × an assumed body mass, CdA by rider type; female values scaled and flagged — see `data/README.md`).

| profile_id | gender | type | mass (kg) | CdA (m²) | P_base (W) | P_threshold (W) | P_max (W) |
|------------|--------|------|----------:|---------:|-----------:|----------------:|----------:|
| `baseline` | — | generic | 75 | 0.26 | 250 | 300 | 400 |
| `male_tt` | M | time trial | 80 | 0.21 | 370 | 400 | 600 |
| `female_tt` | F | time trial | 70 | 0.20 | 260 | 280 | 420 |
| `male_climber` | M | climber | 70 | 0.25 | 325 | 350 | 525 |
| `female_climber` | F | climber | 62 | 0.23 | 230 | 250 | 375 |

`Crr`, `v_max`, and the fatigue tuning constants are shared across riders and stay in the notebook, not the profile.

## Real-world results (validation targets)

The model is checked against the actual 2021 finishing times (machine-readable in `data/real_results.csv`, top three per race):

| Course | Distance | Winner | Time |
|--------|---------:|--------|-----:|
| Tokyo 2021 Olympic ITT (men) | 44.2 km | Primož Roglič | 55:04 |
| Tokyo 2021 Olympic ITT (women) | 22.1 km | Annemiek van Vleuten | 30:13 |
| Flanders 2021 Worlds ITT (men) | 43.3 km | Filippo Ganna | 47:48 |
| Flanders 2021 Worlds ITT (women) | 30.3 km | Ellen van Dijk | 36:05 |

Real ITT winners are time-trial specialists or rouleurs, so these times validate the model's TT-specialist profile. Real races don't produce a separate time per rider *type* (only per rider), so the climber profile is a model exploration, not a measured comparison — the split here is by gender and course, which is all the real data provides.

Sources: Wikipedia — Tokyo [men's](https://en.wikipedia.org/wiki/Cycling_at_the_2020_Summer_Olympics_%E2%80%93_Men's_road_time_trial) / [women's](https://en.wikipedia.org/wiki/Cycling_at_the_2020_Summer_Olympics_%E2%80%93_Women's_road_time_trial), Flanders [men's](https://en.wikipedia.org/wiki/2021_UCI_Road_World_Championships_%E2%80%93_Men's_time_trial) / [women's](https://en.wikipedia.org/wiki/2021_UCI_Road_World_Championships_%E2%80%93_Women's_time_trial). Full top-three times and citations in `references/data-sources.md`.

## Requirements & status

2022 MCM Problem A. Full statement: `references/2022_PowerOfCyclist.pdf`.

**Riders** — *profiles built (`data/rider_profiles.csv`); comparison results in `results/`, paper write-up pending*
- [x] Two rider types — time-trial specialist and climber
- [x] Both genders (male + female of each type)

**Courses** — *course files parameterized; model results in `results/`*
- [x] Tokyo 2021 Olympic ITT — `data/courses/tokyo_olympic_tt.csv`
- [x] Flanders 2021 Worlds ITT — `data/courses/flanders_world_tt.csv`
- [x] Self-designed course (≥4 sharp turns, ≥1 grade, finish near start) — `data/courses/custom_5km_loop.csv`

**Analysis** — *complete; outputs and a re-runnable audit (`results/verify_results.py`) in `results/`*
- [x] Power distribution vs. position that minimizes time — `scipy` optimizes `hill_factor` + `flat_boost` per rider/course; per-segment profile in `results/power_by_segment.csv`, plots in `results/power_*.png`
- [x] Weather sensitivity — wind **strength** (uniform head/tail offset), `results/wind_sensitivity.*`. Wind *direction* is not modeled (the model uses a scalar headwind) — a stated limitation.
- [x] Power-deviation sensitivity (±5/10/15% off the planned power → finishing-time spread) — `results/power_deviation.*`

**Extension**
- [x] Team time trial of six riders (team time set by the fourth finisher) — discussion only (in the write-up)

**Write-up**
- [ ] M142 structure (`docs/paper-outline.md`), not the contest's 25-page format
- [ ] *(Optional, contest-only)* two-page Directeur Sportif race guidance — likely not required for M142; confirm with the professor

The model (`notebooks/model_v5.ipynb`) and the three course files exist. The write-up is a shared document following `docs/paper-outline.md`; the old LaTeX scaffold has been archived under `archive/latex_scaffold/`. With the elite profiles and optimized pacing the model finishes within ~8-12% of the real winners (`results/validation.*`: `male_tt` 2-lap Tokyo 59.2 min vs Roglič 55:04 = +7.5%, `female_tt` Tokyo +11.6%, `male_tt` Flanders +11.9%) — the residual gap is parameter calibration, not structure.

## Running the model

```
git clone https://github.com/wochaotom/Cyclist-Emulator.git
cd Cyclist-Emulator
pip install numpy matplotlib jupyter
jupyter notebook notebooks/model_v5.ipynb
```

Then Run All. Two one-line switches choose what gets simulated:

- **Rider** — in the Rider Parameters cell: `rider = "baseline"` (or `male_tt`, `female_tt`, `male_climber`, `female_climber`).
- **Course** — in the Course Inputs cell: `course_file = "tokyo_olympic_tt.csv"` (or `flanders_world_tt.csv`, `custom_5km_loop.csv`).

Each run prints total time, distance, peak speed, and final fatigue, and plots speed / distance / drag / gradient / fatigue. Step through the rider × course combinations to build the comparison.

## Team

| Name | GitHub | Area |
|------|--------|------|
| Carter Dandridge | @wochaotom | Course parameters |
| Ben Miller | @benmiller74 | Rider model & parameters |
| Dennis Lee | _TBD_ | _TBD_ |
| Prannay Veerabahu | @pveeraba28 | _TBD_ |

Workflow: `CONTRIBUTING.md`. First-time git setup: `START-HERE.md`.
