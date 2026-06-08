# Course Parameterization

*Draft for the write-up — paste into the paper and put it in your own words. Spots marked **[your call]** are where the team should add its own reasoning.*

## How a course is represented

Each course is an ordered list of **segments**. A segment is a stretch of road over which the gradient and conditions are roughly constant, so the model treats them as fixed within the segment. Every segment carries four values:

| Field | Meaning | Source / nature |
|-------|---------|-----------------|
| `distance_m` | Segment length (metres) | **Sourced data** — from the course route (per course, below). |
| `grade_pct` | Average gradient (%, + uphill / − downhill) | **Sourced data** — from the course route (per course, below). |
| `turn_penalty_s` | Fixed time added for braking/cornering on the segment (s) | **Modeling choice** — a flat per-segment cost, not a measured value. Segments are long, so cornering is modeled as a general time penalty rather than per-corner deceleration. |
| `wind_exposure` | `low` / `medium` / `high`, mapped to an effective headwind in the model | **Modeling choice** — assigned from the terrain (exposed/coastal vs. sheltered), not a measured value. |

So **distance and gradient are sourced; the turn penalty and wind label are modeling assignments** the team chose. **[your call]** add a sentence on why a flat turn penalty and a three-level wind label are reasonable at this segment scale.

## The three courses

### 1. Custom course — self-designed 5 km technical loop
*Source: self-designed (no external data).* It meets the problem's own-course requirement: at least four sharp turns, at least one nontrivial gradient, and a finish near the start.

| # | Segment | Distance (m) | Grade (%) | Turn (s) | Wind |
|---|---------|-----:|-----:|-----:|------|
| 1 | Start straight | 800 | 0 | 0 | medium |
| 2 | Sharp right bend | 200 | 0 | 4 | low |
| 3 | Short steep ramp | 600 | 6 | 0 | medium |
| 4 | Hairpin turn | 200 | 2 | 5 | low |
| 5 | Fast descent | 700 | −4 | 0 | medium |
| 6 | Sharp left bend | 200 | 0 | 4 | low |
| 7 | Exposed back straight | 800 | 0 | 0 | high |
| 8 | Chicane | 200 | 0 | 5 | low |
| 9 | Run-in to start | 1300 | −1 | 0 | medium |

Total 5.0 km; four sharp turns (#2, #4, #6, #8); one 6% ramp.

### 2. Tokyo - 2021 Olympic ITT (Fuji Speedway lap)
One 22.1 km lap (the women's course; the men ride two laps = 44.2 km). *Source: a detailed 26-segment reconstruction of the lap from the race course map and elevation profile, with segment distances scaled to the official 22.1 km lap, since no official numeric profile is published. The earlier short-pitch figures (8.9% / 11%) were Cyclingnews preview prose and are no longer used.* **[your call]** note this gives ~310 m of climbing per lap, below the ~423-450 m quoted elsewhere (the simplified profile omits minor undulations); the NBC elevation breakdown and the VeloViewer in-circuit ramp are cross-checks.

| # | Segment | Distance (m) | Grade (%) | Turn (s) | Wind |
|---|---------|-----:|-----:|-----:|------|
| 1 | Speedway start straight | 1679 | 0.0 | 0 | low |
| 2 | Speedway initial descent | 703 | -1.5 | 0 | low |
| 3 | Speedway exit descent (steep) | 681 | -3.5 | 2 | low |
| 4 | Track exit descent upper | 1361 | -3.2 | 2 | low |
| 5 | Track exit descent lower | 1134 | -2.8 | 2 | low |
| 6 | Flat valley bottom / road junction | 567 | 0.2 | 5 | low |
| 7 | Lower slopes of main climb | 1134 | 2.5 | 0 | medium |
| 8 | Main climb lower-mid | 1134 | 3.1 | 0 | medium |
| 9 | Middle of main climb (steepest) | 1021 | 5.8 | 0 | medium |
| 10 | Upper main climb | 1021 | 4.9 | 0 | high |
| 11 | Main climb final steep pitch | 454 | 8.9 | 0 | high |
| 12 | Summit plateau / time check | 340 | 1.0 | 0 | high |
| 13 | Descent from summit (fast upper) | 1134 | -5.1 | 0 | high |
| 14 | Descent mid section | 1134 | -4.6 | 0 | medium |
| 15 | Sweeping bends lower descent | 908 | -4.6 | 3 | medium |
| 16 | Lower descent toward Speedway | 908 | -2.8 | 2 | low |
| 17 | Final flat approach to Speedway | 454 | -1.5 | 0 | low |
| 18 | Flat approach to Speedway entrance | 681 | 0.4 | 6 | low |
| 19 | Pit lane climb (lower ramp) | 454 | 4.2 | 0 | low |
| 20 | Pit lane climb (steep upper) | 340 | 8.9 | 0 | low |
| 21 | Pit lane climb (upper ramp) | 454 | 6.1 | 3 | low |
| 22 | Speedway infield rolling section | 908 | 1.2 | 0 | low |
| 23 | Back straight (flat sheltered) | 1134 | 0.0 | 0 | low |
| 24 | Final bend onto main straight | 454 | 0.3 | 4 | low |
| 25 | Main straight to finish | 1679 | -0.5 | 0 | low |
| 26 | Finish line buffer | 229 | 0.0 | 0 | low |

Total 22.1 km; ~310 m of climbing per lap (men ride two laps = 44.2 km).

### 3. Flanders — 2021 UCI Worlds ITT (Knokke-Heist → Bruges)
Men's 43.3 km (the women's course is 30.3 km). *Source: the distance and the flat profile (~78 m total) are from the official UCI technical guide; the route order (seafront → inland → canals → Bruges) is from the cyclingstage course description. The course is essentially flat, so gradients are 0 and wind exposure is the dominant variable.*

| # | Segment | Distance (m) | Grade (%) | Turn (s) | Wind |
|---|---------|-----:|-----:|-----:|------|
| 1 | Beach seafront start | 1500 | 0 | 0 | high |
| 2 | Sharp turn inland (Knokke-Heist) | 2000 | 0 | 5 | high |
| 3 | Open polder straight (Westkapelle) | 8000 | 0 | 2 | high |
| 4 | Oostkerke section | 5000 | 0 | 3 | medium |
| 5 | Dudzele canal approach | 8000 | 0 | 2 | medium |
| 6 | Boudewijnkanaal into Bruges | 5000 | 0 | 3 | low |
| 7 | Bruges U-turn | 1000 | 0 | 6 | low |
| 8 | Return via Damse Vaart | 9000 | 0 | 3 | medium |
| 9 | Run-in to 't Zand finish | 3800 | 0 | 4 | low |

Total 43.3 km; essentially flat.

## Sourcing summary

- **Distances and gradients** come from route data: Tokyo from a race-course-map reconstruction (scaled to 22.1 km), Flanders from the UCI technical guide (full URLs in `references/data-sources.md`).
- **Tokyo's profile** is anchored to NBC's real elevations (591 → 455 → 676 → 590 → 591 m), giving ~310 m of climbing per lap; no official numeric profile is published.
- **Turn penalties and wind-exposure labels** are modeling choices the team assigned, not measured data.
- **The custom course** is entirely self-designed.
