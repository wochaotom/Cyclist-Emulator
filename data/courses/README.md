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
| `tokyo_olympic_tt.csv` | 2021 Olympic ITT, Tokyo — one 22.1 km lap (women's course; the men ride **2 laps = 44.2 km**). | **First-pass estimate — verify.** |
| `flanders_world_tt.csv` | 2021 UCI Worlds ITT, Flanders — men's **43.3 km** (women's = 30.3 km, shorter). | **First-pass estimate — verify.** |

> ⚠️ **Tokyo and Flanders are first-pass estimates, not measured data.** The total distance, elevation, route order, and wind exposure come from sourced facts (see [`../../references/data-sources.md`](../../references/data-sources.md)), but **per-segment gradients are not published** — the Tokyo profile is *estimated* to match the published ~423 m of climbing per lap, and Flanders is treated as flat (~78 m total). Correct these from a GPX/Strava trace before relying on them in the paper.
