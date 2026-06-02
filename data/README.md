# Data

Empirical data the model uses or is validated against.

- **`real_results.csv`** — real finishing times from the 2021 Tokyo Olympic and Flanders Worlds individual time trials (the validation targets). Columns: `course, event, distance_km, elevation_m, gender, rider, time_s`. Sources and the physiological/physics parameter citations are in [`../references/data-sources.md`](../references/data-sources.md).
- **`courses/`** — course segment files the model reads (see [`courses/README.md`](courses/README.md)).
