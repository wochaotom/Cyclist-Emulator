# Data sources

Sourced values used in the model and for validation. Cite these in the paper.

## Real ITT results (validation targets)

Machine-readable in [`../data/real_results.csv`](../data/real_results.csv).

**2021 Tokyo Olympic ITT** — Fuji Speedway circuit (laps of 22.1 km), rolling/hilly.
- Men's, 44.2 km, ~846 m climbing: Roglič 55:04.19 (3304.19 s), Dumoulin 3365.58 s, Dennis 3368.09 s.
- Women's, 22.1 km, ~423 m: van Vleuten 30:13.49 (1813.49 s), Reusser 1869.96 s, van der Breggen 1875.12 s.
- Sources: [Men's](https://en.wikipedia.org/wiki/Cycling_at_the_2020_Summer_Olympics_%E2%80%93_Men's_road_time_trial), [Women's](https://en.wikipedia.org/wiki/Cycling_at_the_2020_Summer_Olympics_%E2%80%93_Women's_road_time_trial).

**2021 UCI Worlds ITT** — Knokke-Heist → Bruges, flat, coastal, wind-exposed.
- Men's, 43.3 km, ~78 m: Ganna 47:47.83 (2867.83 s, ~54.4 km/h), van Aert 2873.20 s, Evenepoel 2911.17 s.
- Women's, 30.3 km, ~54 m: van Dijk 36:05.28 (2165.28 s), Reusser 2175.57 s, van Vleuten 2189.30 s.
- Sources: [Men's](https://en.wikipedia.org/wiki/2021_UCI_Road_World_Championships_%E2%80%93_Men's_time_trial), [Women's](https://en.wikipedia.org/wiki/2021_UCI_Road_World_Championships_%E2%80%93_Women's_time_trial).

## Physiological and physics parameters (estimates / population ranges)

- **Critical Power (CP):** elite male road cyclists CP ≈ 340 ± 30 W (measured, n=10); female TT ~240–300 W (estimate). [PMC8562202](https://pmc.ncbi.nlm.nih.gov/articles/PMC8562202/)
- **W′ (anaerobic capacity):** ~15.5–24.3 kJ men (method-dependent), ~11–18 kJ women. [PMC8562202](https://pmc.ncbi.nlm.nih.gov/articles/PMC8562202/), [Roadman](https://roadmancycling.com/glossary/w-prime)
- **CdA:** elite TT / aero position ~0.20–0.22 m². [BestBikeSplit](https://www.bestbikesplit.com/blog/cda-aerodynamic-drag-coefficient-cycling)
- **Crr:** road TT tire on good asphalt ~0.003–0.005 (default 0.004). [BestBikeSplit](https://www.bestbikesplit.com/blog/rolling-resistance-cycling-triathlon)

## Course geometry and gradients

- **Tokyo (Fuji Speedway lap):** per-segment climb gradients — main climb 8.9% → 5.9% → 4% → 11% pitch, second climb to 8.9% — from the Cyclingnews ITT previews ([women's](https://www.cyclingnews.com/races/olympic-games-2021/women-s-individual-time-trial/preview/), [men's](https://www.cyclingnews.com/races/olympic-games-2021/men-s-individual-time-trial/preview/)). Men repeat the women's 22.1 km lap. Segment lengths and descent gradients in `tokyo_olympic_tt.csv` are *inferred* to match the published 22.1 km / ~423 m per lap.
- **Flanders:** pan-flat (78 m men / 54 m women, no published climbs). Official km-marked profile in the [UCI Flanders 2021 Technical Guide PDF](https://downloads.ctfassets.net/761l7gh5x5an/lYf25TYStUnbzj6vRXM7f/00f43906c8264b99813bed9102d8bc45/guide-tech-cdmr-flandres-2021-eng-web-md.pdf) (pp. 36–37 men, 42–43 women).
- **Ready-made GPX** (browser export, no login, not scriptable): La Flamme Rouge [Flanders ME ITT](https://www.la-flamme-rouge.eu/maps/viewtrack/414042).

## Not yet verified — confirm before relying on
- Tokyo per-climb gradients (only aggregate ~19 m/km known; per-climb % not published).
- Worlds elevation (single-sourced: men ~78 m, women ~54 m).
- Elite-female measured CP / W′ and CdA (scaled estimates, not lab data).
