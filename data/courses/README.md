# Course files

Each course is a CSV of segments, read by `src/course.py`. One row per segment, in order along the course.

| Column | Meaning |
|--------|---------|
| `segment_id` | Segment number (1, 2, 3, ...) in order. |
| `name` | Short label for the segment. |
| `distance_m` | Segment length in metres. |
| `grade_pct` | Average gradient in percent (+ uphill, − downhill). |
| `turn_penalty_s` | Seconds lost to braking/cornering on this segment (0 if none). |
| `wind_exposure` | `low`, `medium`, or `high` — mapped to an effective headwind in `src/parameters.py`. |

## Courses

| File | Course | Status |
|------|--------|--------|
| `custom_5km_loop.csv` | Self-designed loop — 4 turns, a climb + descent, returns to start. | Ready. |
| `tokyo_olympic_tt.csv` | 2021 Olympic ITT, Tokyo — one 22.1 km lap (women's course; the men ride **2 laps = 44.2 km**). | Climb gradients sourced; lengths/descents inferred. |
| `flanders_world_tt.csv` | 2021 UCI Worlds ITT, Flanders — men's **43.3 km** (women's = 30.3 km, shorter). | Confirmed pan-flat. |

> ℹ️ **Provenance.** Tokyo's climb gradients (main climb 8.9 → 5.9 → 4 → 11%, second climb to 8.9%) are quoted from the Cyclingnews ITT previews — but the **segment lengths and descent gradients are inferred** to match the published 22.1 km lap and ~423 m of climbing. Flanders is **pan-flat** (78 m over 43.3 km, no published climbs), so the flat profile is appropriate; the official UCI technical guide has the km-marked profile. Full sources: [`../../references/data-sources.md`](../../references/data-sources.md).
>
> For an exact route, the clean GPX is on La Flamme Rouge (browser **Export GPX**, no login). Drop it in a `raw/` folder here and I'll convert it to the CSV.
