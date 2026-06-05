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

`notebooks/model_v3.ipynb`. The rider and bike are treated as one point mass, pushed forward by the rider against air, road, and gravity, and stepped forward in time.

On a segment of slope angle $\theta = \arctan(\text{grade}\%/100)$, the resisting forces are aerodynamic drag, rolling resistance, and gravity:

$$F_\text{drag} = \tfrac{1}{2}\,\rho\,C_dA\,(v+w)^2, \quad F_\text{roll} = C_{rr}\,m\,g\cos\theta, \quad F_\text{grav} = m\,g\sin\theta$$

where $v$ is speed and $w$ the effective headwind from the segment's wind label. The rider's propulsive force is power divided by speed, $F_\text{rider} = P_\text{out}/\max(v,\,0.5)$ (the floor avoids dividing by zero at the start). Net force is integrated forward with a one-second step:

$$F_\text{net} = F_\text{rider} - F_\text{drag} - F_\text{roll} - F_\text{grav}, \qquad v \leftarrow \mathrm{clamp}\!\left(v + \tfrac{\Delta t}{m}F_\text{net},\ 0,\ v_\text{max}\right), \qquad x \leftarrow x + v\,\Delta t$$

Target power rises with gradient (harder uphill, easier down) and is capped by a fatigue-reduced ceiling:

$$P_\text{target} = \max(50,\ P_\text{base} + k_\text{hill}\,\theta), \qquad P_\text{out} = \min\!\big(P_\text{target},\ P_\text{max}(1 - c_\text{fat}\cdot\text{fat})\big)$$

Fatigue grows when output exceeds a threshold and recovers below it (clamped to $[0,1]$):

$$\Delta\text{fat} = \begin{cases} +\,r_\text{fat}\left(\dfrac{P_\text{out}-P_\text{thr}}{P_\text{thr}}\right)^2 \Delta t & P_\text{out} > P_\text{thr} \\[2mm] -\,r_\text{rec}\,\Delta t & \text{otherwise} \end{cases}$$

Each segment also adds its `turn_penalty_s` to the clock for cornering. Symbols map to code as $\rho$ = `a_density`, $C_dA$ = `CdA`, $C_{rr}$ = `Crr`, $k_\text{hill}$ = `hill_factor`, $P_\text{thr}$ = `P_threshold`, $c_\text{fat}$ = `fatigue_impact`, $r_\text{fat}$ = `fatigue_rate`, $r_\text{rec}$ = `recovery_rate`. Parameter values and their justification are in the team write-up.

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
| `tokyo_olympic_tt.csv` | Tokyo 2021 Olympic ITT (1 lap; men ride 2) | 22.1 km | ~390 m | NBC elevation breakdown |
| `flanders_world_tt.csv` | Flanders 2021 Worlds ITT (men) | 43.3 km | ~78 m (flat) | UCI technical guide |

Distance and gradient are sourced; turn penalty and wind label are modeling assignments. Per-field provenance is in `data/courses/README.md` and `references/data-sources.md`.

## Requirements & status

2022 MCM Problem A. Detailed statement: `docs/problem.md` and `references/2022_PowerOfCyclist.pdf`.

**Riders**
- [ ] Two rider types — a time-trial specialist and one other (climber / sprinter / rouleur / puncheur)
- [ ] Both genders

**Courses** — *course files parameterized; model results not yet produced*
- [x] Tokyo 2021 Olympic ITT — `data/courses/tokyo_olympic_tt.csv`
- [x] Flanders 2021 Worlds ITT — `data/courses/flanders_world_tt.csv`
- [x] Self-designed course (≥4 sharp turns, ≥1 grade, finish near start) — `data/courses/custom_5km_loop.csv`

**Analysis**
- [ ] Power distribution vs. position that minimizes time
- [ ] Weather (wind) sensitivity
- [ ] Power-deviation sensitivity (missed target power → split-time range)

**Extension**
- [ ] Team time trial of six riders (team time set by the fourth finisher) — discussion only

**Write-up**
- [ ] M142 structure (`docs/paper-outline.md`), not the contest's 25-page format

The model (`notebooks/model_v3.ipynb`) and the three course files exist. Earlier figures/tables in `paper/` came from the retired CP/W′ model and do not carry over. The model currently predicts times well above the real results in `data/real_results.csv` — a parameter-calibration item, not a structural one.

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
