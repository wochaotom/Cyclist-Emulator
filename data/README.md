# Data

Empirical data the model uses or is validated against.

- **`real_results.csv`** — real finishing times from the 2021 Tokyo Olympic and Flanders Worlds individual time trials (the validation targets). Columns: `course, event, distance_km, elevation_m, gender, rider, time_s`. Sources and the physiological/physics parameter citations are in [`../references/data-sources.md`](../references/data-sources.md).
- **`rider_profiles.csv`** — rider parameter sets the model loads (one row per profile). Columns: `profile_id, gender, rider_type, mass_kg, cda_m2, p_base_w, p_threshold_w, p_max_w`. Switch profiles by setting `rider = "..."` in the notebook's Rider Parameters cell. `baseline` reproduces the originally submitted rider; `male_tt` / `female_tt` / `male_climber` / `female_climber` are derived from the sourced ranges (sustainable power = W/kg from Valenzuela 2022 / Mateo-March 2022 × an assumed body mass; CdA by rider type from García-López, with female values scaled and flagged; masses assumed). `Crr`, `v_max`, and the fatigue tuning constants are not rider-specific and stay in the notebook. Basis and citations: [`../references/data-sources.md`](../references/data-sources.md).
- **`courses/`** — course segment files the model reads (see [`courses/README.md`](courses/README.md)).
