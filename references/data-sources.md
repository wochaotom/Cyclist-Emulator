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

## Rider and physics parameters (estimates / population ranges)

These map to the **canonical model's** inputs ([`../notebooks/model_v3.ipynb`](../notebooks/model_v3.ipynb)). Deduped citation list: [`references.md`](references.md).

- **Sustainable / threshold power** (the model's `P_base` / `P_threshold`): elite men ≈ 5.5 W/kg for 60 min (~360–400 W at typical TT mass); elite women ≈ 4.2 W/kg (~260–290 W). Measured critical power for elite men ≈ 324–365 W. [Valenzuela 2022, PMID 35193109](https://pubmed.ncbi.nlm.nih.gov/35193109/) (men, n=144 pros); [Mateo-March 2022, PMID 35168197](https://pubmed.ncbi.nlm.nih.gov/35168197/) (women, n=44 pros); [Clark & MacDermid 2021, PMC8562202](https://pmc.ncbi.nlm.nih.gov/articles/PMC8562202/).
- **Peak / ceiling power** (the model's `P_max`): world-class FTP ≈ 6.4 (men) / 5.7 (women) W/kg; 5-s peak ≈ 24 / 19 W/kg. [Coggan & Allen power-profile chart](https://www.cyclinganalytics.com/blog/2018/06/how-does-your-cycling-power-output-compare).
- **CdA (drag area, TT position):** TT specialist ≈ 0.20–0.23 m²; climber/road position ≈ 0.24–0.27 m². [García-López 2008, doi:10.1080/02640410701501697](https://doi.org/10.1080/02640410701501697) (wind tunnel, pros); [BestBikeSplit](https://www.bestbikesplit.com/blog/cda-aerodynamic-drag-coefficient-cycling).
- **Crr (rolling resistance), road TT tire on tarmac:** ≈ 0.003 (fastest tire / pristine) to 0.004 (on-road); default 0.004. [bicyclerollingresistance.com](https://www.bicyclerollingresistance.com/road-bike-reviews/continental-grand-prix-5000-tt-tr); [SILCA](https://silca.cc/blogs/silca/part-4b-rolling-resistance-and-impedance).
- **Air density (ρ):** 1.225 kg/m³, assumed constant per course (International Standard Atmosphere: dry air, 15 °C, sea level). Used in the aerodynamic-drag term; real density runs a few percent lower at Fuji Speedway's ~600 m elevation, which the model treats as negligible (a stated assumption, not a measured value).
- **Max descent speed** (the model's `V_max`): ceiling ≈ 100–110 km/h (Politt 101.5 km/h on official Tour telemetry). [BikeRadar](https://www.bikeradar.com/features/tour-de-france-2019-in-numbers).
- **Bike mass:** ≈ 7–14 kg. [Bicycle Warehouse](https://bicyclewarehouse.com/blogs/news/how-much-does-a-bicycle-weigh).
- *Tuning constants* (`hill_factor`, `fatigue_rate`, `recovery_rate`, `fatigue_impact`) are model choices — justified in the write-up, not externally sourced.

**For the alternative CP/W′ model only** (archived, [`../archive/cp_w_prime_model/`](../archive/cp_w_prime_model/)):
- **Critical Power (CP) and W′ (anaerobic work capacity):** trained men W′ ≈ 12.7 ± 3.4 kJ, CP ≈ 301 ± 35 W; broader athlete range ~14–28 kJ. [Bartram 2018, PMC7560916](https://pmc.ncbi.nlm.nih.gov/articles/PMC7560916/); [Clark & MacDermid 2021, PMC8562202](https://pmc.ncbi.nlm.nih.gov/articles/PMC8562202/).

## Course geometry and gradients

- **Tokyo (Fuji Speedway lap):** gradients in `tokyo_olympic_tt.csv` are derived from the [NBC Olympics elevation breakdown](https://www.nbcolympics.com/news/cycling-101-courses) (real elevations at stated distances: 591 → 455 → 676 → 590 → 591 m), giving ~390 m of climbing per lap. No official numeric profile is published; the earlier Cyclingnews preview pitches (8.9%/11%) were prose and are not used. Men repeat the women's 22.1 km lap. In-circuit ramp cross-check: [VeloViewer Fuji Speedway segment](https://veloviewer.com/segments/16466365) (0.86 km / 4.4%).
- **Flanders:** pan-flat (78 m men / 54 m women, no published climbs). Official km-marked profile in the [UCI Flanders 2021 Technical Guide PDF](https://downloads.ctfassets.net/761l7gh5x5an/lYf25TYStUnbzj6vRXM7f/00f43906c8264b99813bed9102d8bc45/guide-tech-cdmr-flandres-2021-eng-web-md.pdf) (pp. 36–37 men, 42–43 women).
- **Ready-made GPX** (browser export, no login, not scriptable): La Flamme Rouge [Flanders ME ITT](https://www.la-flamme-rouge.eu/maps/viewtrack/414042).

## Not yet verified — confirm before relying on
- Tokyo has no official numeric profile; gradients come from the NBC elevation breakdown. Modeled gain (~390 m/lap) is below the ~423 m/lap implied by the quoted 846 m / 2 laps — a ±40 m gap from undulations the simplified profile omits.
- Worlds elevation (single-sourced: men ~78 m, women ~54 m).
- Elite-female CdA and W′ (scaled from male lab data). Female *threshold power* is now sourced (Mateo-March 2022, n=44 pros).
