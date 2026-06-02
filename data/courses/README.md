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

`custom_5km_loop.csv` is a worked example. Real courses (time-trial routes, etc.) get added here as we parameterise them.
