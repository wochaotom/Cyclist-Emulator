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

### 2. Tokyo — 2021 Olympic ITT (Fuji Speedway lap)
One 22.1 km lap (the women's course; the men ride two laps = 44.2 km). *Source: the climb gradients are quoted from the Cyclingnews race preview; the segment lengths and descents are estimated to match the published lap distance (22.1 km) and total climbing (~423 m per lap), because no usable official elevation profile was available.* **[your call]** add the Cyclingnews citation.

| # | Segment | Distance (m) | Grade (%) | Turn (s) | Wind |
|---|---------|-----:|-----:|-----:|------|
| 1 | Speedway start and exit descent | 4000 | −3.5 | 6 | low |
| 2 | Flat approach | 1500 | 0 | 2 | medium |
| 3 | Main climb lower (steep) | 1000 | 8.9 | 0 | medium |
| 4 | Main climb middle | 1000 | 5.9 | 0 | medium |
| 5 | Main climb upper | 800 | 4.0 | 0 | medium |
| 6 | Main climb final pitch | 300 | 11.0 | 0 | low |
| 7 | Descent from peak | 4000 | −5.0 | 4 | medium |
| 8 | Flat valley | 1500 | 0 | 2 | medium |
| 9 | Second climb lower | 1200 | 5.0 | 2 | medium |
| 10 | Second climb pit-lane pitch | 800 | 8.9 | 3 | low |
| 11 | Rolling rise | 1500 | 3.0 | 0 | medium |
| 12 | Descent to finish area | 1660 | −5.0 | 3 | low |
| 13 | Late undulation | 1000 | 3.4 | 0 | low |
| 14 | Finish straight | 1840 | 0 | 0 | low |

Total 22.1 km; ~423 m of climbing per lap.

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

- **Distances and gradients** come from route data: Tokyo from the Cyclingnews race preview, Flanders from the UCI technical guide (full URLs in `references/references.md`).
- **Tokyo's segment lengths and descents** are estimated to match the published 22.1 km / ~423 m totals, since no usable official elevation profile was found.
- **Turn penalties and wind-exposure labels** are modeling choices the team assigned, not measured data.
- **The custom course** is entirely self-designed.
