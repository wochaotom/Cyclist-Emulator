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
| `custom_5km_loop.csv` | Self-designed loop (4 turns, a climb + descent, returns to start). | Worked example, ready. |
| `tokyo_olympic_tt.csv` | 2021 Olympic individual time trial, Tokyo. | Template — fill from the real route. |
| `flanders_world_tt.csv` | 2021 UCI Worlds individual time trial, Flanders. | Template — fill from the real route. |

The two real courses are required by the problem. Add the segment breakdown (distances, grades, turns, wind) from public route data during course parameterization.
