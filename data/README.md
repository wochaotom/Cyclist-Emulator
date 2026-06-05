# Data

Empirical data the model uses or is validated against.

## `real_results.csv`

Real finishing times from the 2021 Tokyo Olympic and Flanders Worlds individual time trials — the validation targets the model is checked against.

| Column | Meaning |
|--------|---------|
| `course` | `tokyo_2021` / `flanders_2021`. |
| `event` | `olympic_itt` / `worlds_itt`. |
| `distance_km` | Course length for that result (men's and women's differ). |
| `elevation_m` | Quoted total climbing for that course/gender. |
| `gender` | `M` / `F`. |
| `rider` | Finisher's name. |
| `time_s` | Finishing time, seconds. |

Sources for the results and the physical/physiological parameters: [`../references/data-sources.md`](../references/data-sources.md).

## `rider_profiles.csv`

Rider parameter sets the model loads — one row per profile, selected by `rider = "..."` in the notebook's Rider Parameters cell.

| Column | Meaning |
|--------|---------|
| `profile_id` | Name used to select the rider (e.g. `rider = "male_tt"`). |
| `gender` | `M` / `F` / `unspecified` — descriptive label, not used in the math. |
| `rider_type` | `time_trial` / `climber` / `generic` — descriptive label, not used in the math. |
| `mass_kg` | Total rider + bike mass (kg) → the model's `m`. |
| `cda_m2` | Drag area (m²); lower is more aerodynamic → `CdA`. |
| `p_base_w` | Flat-ground target power (W) → `P_base`. |
| `p_threshold_w` | Power above which fatigue accumulates (W) → `P_threshold`. |
| `p_max_w` | Short-duration maximal power ceiling (W) → `P_max`. |

`baseline` reproduces the originally submitted rider; the typed profiles (`male_tt`, `female_tt`, `male_climber`, `female_climber`) come from the sourced ranges — power is a W/kg figure (Valenzuela 2022 men, Mateo-March 2022 women) times an assumed body mass; CdA is by rider type (García-López, with female values scaled and flagged); masses are assumed. `Crr`, `v_max`, and the fatigue tuning constants are not rider-specific and stay in the notebook. Basis and citations: [`../references/data-sources.md`](../references/data-sources.md).

## `courses/`

Course segment files the model reads, one CSV per course — see [`courses/README.md`](courses/README.md).
