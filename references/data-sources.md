# Data sources

The single sources file for the project — every sourced value behind the model and the validation, with citations ready to format into the paper's reference list.

## Real ITT results (validation targets)

Machine-readable in [`../data/real_results.csv`](../data/real_results.csv).

**2021 Tokyo Olympic ITT** — Fuji Speedway circuit (laps of 22.1 km), rolling/hilly.
- Men's, 44.2 km, ~846 m climbing: Roglič 55:04.19 (3304.19 s), Dumoulin 3365.58 s, Dennis 3368.09 s.
- Women's, 22.1 km, ~423 m: van Vleuten 30:13.49 (1813.49 s), Reusser 1869.96 s, van der Breggen 1875.12 s.
- Sources: Wikipedia [men's](https://en.wikipedia.org/wiki/Cycling_at_the_2020_Summer_Olympics_%E2%80%93_Men's_road_time_trial) / [women's](https://en.wikipedia.org/wiki/Cycling_at_the_2020_Summer_Olympics_%E2%80%93_Women's_road_time_trial); official host (JS-rendered, cross-check) olympics.com [men](https://www.olympics.com/en/olympic-games/tokyo-2020/results/cycling-road/men-s-individual-time-trial) / [women](https://www.olympics.com/en/olympic-games/tokyo-2020/results/cycling-road/women-s-individual-time-trial).

**2021 UCI Worlds ITT** — Knokke-Heist → Bruges, flat, coastal, wind-exposed.
- Men's, 43.3 km, ~78 m: Ganna 47:47.83 (2867.83 s, ~54.4 km/h), van Aert 2873.20 s, Evenepoel 2911.17 s.
- Women's, 30.3 km, ~54 m: van Dijk 36:05.28 (2165.28 s), Reusser 2175.57 s, van Vleuten 2189.30 s.
- Sources: Wikipedia [men's](https://en.wikipedia.org/wiki/2021_UCI_Road_World_Championships_%E2%80%93_Men's_time_trial) / [women's](https://en.wikipedia.org/wiki/2021_UCI_Road_World_Championships_%E2%80%93_Women's_time_trial); Cyclingnews [men](https://www.cyclingnews.com/races/uci-road-world-championships-2021/men-elite-individual-time-trial/results/) / [women](https://www.cyclingnews.com/races/uci-road-world-championships-2021/women-elite-individual-time-trial/results/).

## Rider and physics parameters (estimates / population ranges)

These map to the **canonical model's** inputs ([`../notebooks/model_v5.ipynb`](../notebooks/model_v5.ipynb)).

- **Sustainable / threshold power** (the model's `P_base` / `P_threshold`): elite men ≈ 5.5 W/kg for 60 min (~360–400 W at typical TT mass); elite women ≈ 4.2 W/kg (~260–290 W). Measured critical power for elite men ≈ 324–365 W. [Valenzuela 2022, PMID 35193109](https://pubmed.ncbi.nlm.nih.gov/35193109/) (men, n=144 pros); [Mateo-March 2022, PMID 35168197](https://pubmed.ncbi.nlm.nih.gov/35168197/) (women, n=44 pros); [Clark & MacDermid 2021, PMC8562202](https://pmc.ncbi.nlm.nih.gov/articles/PMC8562202/).
- **Peak / ceiling power** (the model's `P_max`): world-class FTP ≈ 6.4 (men) / 5.7 (women) W/kg; 5-s peak ≈ 24 / 19 W/kg. [Coggan & Allen power-profile chart](https://www.cyclinganalytics.com/blog/2018/06/how-does-your-cycling-power-output-compare).
- **CdA (drag area, TT position):** TT specialist ≈ 0.20–0.23 m²; climber/road position ≈ 0.24–0.27 m². [García-López 2008, doi:10.1080/02640410701501697](https://doi.org/10.1080/02640410701501697) (wind tunnel, pros); [Frontiers in Sports & Active Living 2025, doi:10.3389/fspor.2025.1599319](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2025.1599319/full); [BestBikeSplit](https://www.bestbikesplit.com/blog/cda-aerodynamic-drag-coefficient-cycling). No measured female-specific TT CdA exists in the published literature; any female value is scaled from male/anthropometric data (estimate, not measured).
- **Crr (rolling resistance), road TT tire on tarmac:** ≈ 0.003 (fastest tire / pristine) to 0.004 (on-road); default 0.004. [bicyclerollingresistance.com](https://www.bicyclerollingresistance.com/road-bike-reviews/continental-grand-prix-5000-tt-tr); [SILCA](https://silca.cc/blogs/silca/part-4b-rolling-resistance-and-impedance).
- **Air density (ρ):** 1.225 kg/m³, assumed constant per course (International Standard Atmosphere: dry air, 15 °C, sea level). Used in the aerodynamic-drag term; real density runs a few percent lower at Fuji Speedway's ~600 m elevation, which the model treats as negligible (a stated assumption, not a measured value).
- **Gravitational acceleration (g):** 9.81 m/s² — standard gravity (the model's `g`, used in the gravity and rolling-resistance terms).
- **Max descent speed** (the model's `V_max`): ceiling ≈ 100–110 km/h (Politt 101.5 km/h on official Tour telemetry; the 130 km/h figures are uncorrected Strava — do not use). [BikeRadar](https://www.bikeradar.com/features/tour-de-france-2019-in-numbers).
- **Bike mass:** ≈ 7–14 kg; a race TT bike sits at the light end (the model uses ~8 kg). [Bicycle Warehouse](https://bicyclewarehouse.com/blogs/news/how-much-does-a-bicycle-weigh).
- **Effective headwind (`wind_map`):** `low` / `medium` / `high` wind exposure maps to 0.5 / 1.0 / 2.0 m/s — a modeling assignment from terrain (exposed/coastal vs. sheltered), not a measured value.
- *Tuning constants* (`hill_factor`, `fatigue_rate`, `recovery_rate`, `fatigue_impact`) are model choices — justified in the write-up, not externally sourced (see "Dropped after verification" below).

**For the alternative CP/W′ model only** (archived, [`../archive/cp_w_prime_model/`](../archive/cp_w_prime_model/)):
- **Critical Power (CP) and W′ (anaerobic work capacity):** trained men W′ ≈ 12.7 ± 3.4 kJ, CP ≈ 301 ± 35 W; broader athlete range ~14–28 kJ. [Bartram 2018, PMC7560916](https://pmc.ncbi.nlm.nih.gov/articles/PMC7560916/); [Clark & MacDermid 2021, PMC8562202](https://pmc.ncbi.nlm.nih.gov/articles/PMC8562202/). No clean elite-female absolute W′ dataset exists; women's W′ is approximate (~10–18 kJ), partly from secondary sources — treat as an estimate.

## Course geometry and gradients

- **Tokyo (Fuji Speedway lap):** no official numeric profile is published, so this entry is a reconstruction. `tokyo_olympic_tt.csv` is a detailed 26-segment lap reconstructed from the race course map and elevation profile, with segment distances **scaled to the official 22.1 km lap** (~310 m of climbing per lap); the men ride two laps (44.2 km), the women one. Cross-check elevations: the [NBC Olympics breakdown](https://www.nbcolympics.com/news/cycling-101-courses) (591 → 455 → 676 → 590 → 591 m). **Quoted totals conflict:** cyclingstage/Wikipedia give ~846 m for the men's two laps (≈423 m/lap), UCI's own preview ~900 m (≈450 m/lap), and the official UCI/IOC release gives no figure — all above the modeled ~310 m/lap, so the paper should disclose the spread rather than assert one value. The earlier Cyclingnews preview pitches (8.9%/11%) were prose and are not used, and the VeloViewer/PJAMM "Fuji" climbs are the road race, not the TT. In-circuit ramp cross-check: [VeloViewer Fuji Speedway segment](https://veloviewer.com/segments/16466365) (0.86 km / 4.4%). Route narrative: [UCI](https://www.uci.org/article/olympic-gold-awaits-at-the-foot-of-mount-fuji/55jtcCLEgwlDZr0WXhDvcv), [cyclingstage](https://www.cyclingstage.com/summer-olympics-2021/route-itt-tokyo-2021/).
- **Flanders:** pan-flat (78 m men / 54 m women, no published climbs). Official km-marked profile in the [UCI Flanders 2021 Technical Guide PDF](https://downloads.ctfassets.net/761l7gh5x5an/lYf25TYStUnbzj6vRXM7f/00f43906c8264b99813bed9102d8bc45/guide-tech-cdmr-flandres-2021-eng-web-md.pdf) (pp. 36–37 men, 42–43 women). Route description: [cyclingstage](https://www.cyclingstage.com/world-championships-2021-flanders/route-itt-wc-2021/). Official GPX: [flanders2021.com](https://www.flanders2021.com/en/ride-knokke-heist-brugge).
- **Ready-made GPX** (browser export, no login, not scriptable): La Flamme Rouge [Flanders ME ITT](https://www.la-flamme-rouge.eu/maps/viewtrack/414042).

## Verification notes
- **Flanders elevation — confirmed** (men 78 m / women 54 m) against multiple sources and the official UCI technical guide.
- **Tokyo gain — no authoritative figure exists; sources conflict** (see the Tokyo entry above). Disclose the ~390 (modeled) / ~423 / ~450 m spread in the paper rather than asserting one value.
- **Female CdA and W′ — no measured female-specific values exist** in the literature; both are scaled/estimated from male data and labeled as such above.

## Dropped after verification
- **PMC10915604** (a 4-subject *triathlon* study, not a TT-cyclist threshold) and the **Medical News Today / Harvard "calories-burned"** basis for `P_base`/`P_max` (that figure is *metabolic* energy, ~4–5× the mechanical power at the pedals) were both rejected and replaced by the studies in the parameters section above.
- The tuning constants (`hill_factor`, `fatigue_rate`, `recovery_rate`, `fatigue_impact`) are model choices, not externally sourced — justify them in the text, don't cite them.
- **Sprint-records check:** the write-up's attempt to source `fatigue_rate` from "sprint world records (20 m / 50 m)" does **not** hold — those records are ~1–3 s efforts and peak/sprint power is sustainable only ~1–5 s, not the ~30 s assumed (a ~30 s all-out effort is an above-critical-power anaerobic effort at *sub-maximal* power, governed by W′). Keep `fatigue_rate` as a tuned choice; if a duration anchor is wanted, cite the power–duration literature ([PMC10218722](https://pmc.ncbi.nlm.nih.gov/articles/PMC10218722/), [PMC6383108](https://pmc.ncbi.nlm.nih.gov/articles/PMC6383108/)) and relabel the 30 s regime accordingly.
