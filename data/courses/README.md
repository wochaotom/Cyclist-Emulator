# Course files

Each course is a CSV of segments, read by the model. One row per segment, in order along the course.

| Column | Meaning |
|--------|---------|
| `segment_id` | Segment number (1, 2, 3, ...) in order. |
| `name` | Short label for the segment. |
| `distance_m` | Segment length in metres. |
| `grade_pct` | Average gradient in percent (+ uphill, − downhill). |
| `turn_penalty_s` | Seconds lost to braking/cornering on this segment (0 if none). |
| `wind_exposure` | `low`, `medium`, or `high` — mapped to an effective headwind in the model. |

## Courses

| File | Course | Status |
|------|--------|--------|
| `custom_5km_loop.csv` | Self-designed **technical loop** — 4 sharp turns, a short steep ramp, returns to start. | Ready. |
| `tokyo_olympic_tt.csv` | 2021 Olympic ITT, Tokyo — one 22.1 km lap (women's course; the men ride **2 laps = 44.2 km**). | Gradients from the NBC elevation breakdown. |
| `flanders_world_tt.csv` | 2021 UCI Worlds ITT, Flanders — men's **43.3 km** (women's = 30.3 km, shorter). | Confirmed pan-flat. |

> ℹ️ **Provenance.** Tokyo's gradients are derived from the NBC Olympics elevation breakdown (real elevations at stated distances: 591 → 455 → 676 → 590 → 591 m), giving ~390 m of climbing per lap; no official numeric profile is published. Flanders is **pan-flat** (78 m over 43.3 km), from the official UCI technical guide. Full sources: [`../../references/data-sources.md`](../../references/data-sources.md).
>
> For an exact route, the clean GPX is on La Flamme Rouge (browser **Export GPX**, no login). Drop it in a `raw/` folder here and I'll convert it to the CSV.
