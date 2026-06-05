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

### How the typed profiles were derived

Each typed profile is a literature-anchored estimate, not a measured athlete. Sustainable power is a published W/kg figure times an assumed body mass; `P_base` ≈ 0.93 × `P_threshold` (flat-ground power held just under threshold, so flat riding does not build fatigue); `P_max` ≈ 1.5 × `P_threshold` (a nominal short-effort ceiling that rarely binds on these courses); `CdA` is the wind-tunnel range for the rider type, with the female values scaled down ~10% (no measured female TT CdA exists in the literature). Body masses are assumptions — TT specialists heavier, climbers lighter, women lighter — plus a ~8 kg bike (the light end of the sourced 7–14 kg range — a race TT bike sits near the bottom; range cited to Bicycle Warehouse in [`../references/data-sources.md`](../references/data-sources.md)).

| Profile | Body + bike (kg) | W/kg → P_threshold | P_base (≈0.93×) | P_max (≈1.5×) | CdA |
|---------|-----------------:|--------------------|----------------:|--------------:|-----|
| `male_tt` | ~72 + 8 = 80 | 5.5 × 72 ≈ 400 W (Valenzuela 2022) | 370 | 600 | 0.21 (TT, García-López) |
| `male_climber` | ~62 + 8 = 70 | 5.6 × 62 ≈ 350 W (Valenzuela 2022) | 325 | 525 | 0.25 (road/climb) |
| `female_tt` | ~62 + 8 = 70 | 4.5 × 62 ≈ 280 W (Mateo-March 2022) | 260 | 420 | 0.20 (TT, scaled) |
| `female_climber` | ~54 + 8 = 62 | 4.6 × 54 ≈ 250 W (Mateo-March 2022) | 230 | 375 | 0.23 (road/climb, scaled) |

`baseline` (75 kg, CdA 0.26, P_base/P_threshold/P_max = 250/300/400 W) is the originally submitted placeholder rider, kept so the first result stays reproducible — it is not derived from these sources. Full citations: [`../references/data-sources.md`](../references/data-sources.md).

## `courses/`

Course segment files the model reads, one CSV per course — see [`courses/README.md`](courses/README.md).
