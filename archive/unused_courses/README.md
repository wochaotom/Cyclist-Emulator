# Unused courses

Earlier Tokyo course reconstructions, kept for reference. Neither is read by the
model — the canonical Tokyo course is [`../../data/courses/tokyo_olympic_tt.csv`](../../data/courses/tokyo_olympic_tt.csv)
(26-segment lap reconstructed from the race course map and elevation profile,
scaled to the official 22.1 km lap; the men ride two laps via the notebook's
`laps` switch).

| File | What it was | Why it was dropped |
|------|-------------|--------------------|
| `tokyo_mens_course.csv` | 52-segment, two-lap reconstruction (39.0 km total, ~19.5 km/lap, ~546 m climb). | The lap came out ~19.5 km, well short of the official 22.1 km; superseded by the scaled 22.1 km lap. |
| `tokyo_olympic_tt_more_detail.csv` | 18-segment, single-lap reconstruction (21.3 km, ~312 m climb). | Coarser than, and slightly short of, the 22.1 km canonical lap; superseded. |

The canonical lap is 22.1 km because that is the published Olympic ITT lap distance
(Wikipedia / cyclingstage, matching `../../data/real_results.csv`). See
[`../../references/data-sources.md`](../../references/data-sources.md) for the full sourcing.
