# References

Deduped source list behind the course data and the model's parameters — ready to format into the paper's reference section. (`data-sources.md` has the same links with more context.)

## Courses, routes, and race results
- **2021 Tokyo Olympic ITT** — men's results & route. Wikipedia: https://en.wikipedia.org/wiki/Cycling_at_the_2020_Summer_Olympics_–_Men's_road_time_trial
- **2021 Tokyo Olympic ITT** — women's results & route. Wikipedia: https://en.wikipedia.org/wiki/Cycling_at_the_2020_Summer_Olympics_–_Women's_road_time_trial
- Tokyo ITT course preview / climb gradients. Cyclingnews: https://www.cyclingnews.com/races/olympic-games-2021/men-s-individual-time-trial/preview/ and https://www.cyclingnews.com/races/olympic-games-2021/women-s-individual-time-trial/preview/
- Tokyo ITT distance & elevation. cyclingstage: https://www.cyclingstage.com/summer-olympics-2021/route-itt-tokyo-2021/
- **2021 UCI Worlds ITT (Flanders)** — men's & women's results. Wikipedia: https://en.wikipedia.org/wiki/2021_UCI_Road_World_Championships_–_Men's_time_trial and https://en.wikipedia.org/wiki/2021_UCI_Road_World_Championships_–_Women's_time_trial
- Flanders ITT route. cyclingstage: https://www.cyclingstage.com/world-championships-2021-flanders/route-itt-wc-2021/
- Flanders ITT official course + elevation profile. UCI Technical Guide (PDF): https://downloads.ctfassets.net/761l7gh5x5an/lYf25TYStUnbzj6vRXM7f/00f43906c8264b99813bed9102d8bc45/guide-tech-cdmr-flandres-2021-eng-web-md.pdf

## Rider physiology and physics

**Sustainable / threshold power (FTP, CP) — elite cyclists**
- Valenzuela et al. 2022, *Int. J. Sports Physiol. Perform.* 17(5):701–710 — men, n=144 pros. PMID 35193109: https://pubmed.ncbi.nlm.nih.gov/35193109/
- Mateo-March et al. 2022, *IJSPP* 17(5):682–689 — women, n=44 pros. PMID 35168197: https://pubmed.ncbi.nlm.nih.gov/35168197/
- Clark & MacDermid 2021 (measured critical power). PMC8562202: https://pmc.ncbi.nlm.nih.gov/articles/PMC8562202/
- → 60-min ≈ 5.5 W/kg (men) / 4.2 W/kg (women); measured CP ≈ 324–365 W for elite men.

**Peak power (P_max) / power-profile ceiling**
- Coggan & Allen power-profile chart (world-class row), via Cycling Analytics: https://www.cyclinganalytics.com/blog/2018/06/how-does-your-cycling-power-output-compare
- → world-class FTP ≈ 6.4 (men) / 5.7 (women) W/kg; 5-s peak ≈ 24 / 19 W/kg.

**CdA (drag area, TT position)**
- García-López, Padilla et al. 2008, *J. Sports Sci.* 26(3):277–286 — wind tunnel, pros. doi:10.1080/02640410701501697
- Frontiers in Sports & Active Living 2025, doi:10.3389/fspor.2025.1599319: https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2025.1599319/full
- BestBikeSplit (practical ranges): https://www.bestbikesplit.com/blog/cda-aerodynamic-drag-coefficient-cycling
- → TT specialist ≈ 0.20–0.23 m²; climber/road position ≈ 0.24–0.27 m².

**Rolling resistance (Crr), road TT tire on tarmac**
- bicyclerollingresistance.com (lab drum tests): https://www.bicyclerollingresistance.com/road-bike-reviews/continental-grand-prix-5000-tt-tr
- SILCA rolling-resistance methodology: https://silca.cc/blogs/silca/part-4b-rolling-resistance-and-impedance
- BestBikeSplit: https://www.bestbikesplit.com/blog/rolling-resistance-cycling-triathlon
- → ≈ 0.003 (pristine surface / fastest tire) to 0.004 (on-road).

**Max descent speed (V_max)**
- BikeRadar, 2019 Tour de France telemetry — Politt 101.5 km/h, first over 100 km/h on the official feed: https://www.bikeradar.com/features/tour-de-france-2019-in-numbers
- → defensible ceiling ≈ 100–110 km/h. (130 km/h figures are uncorrected Strava — do not use as a default.)

**Bike mass**
- Bicycle Warehouse: https://bicyclewarehouse.com/blogs/news/how-much-does-a-bicycle-weigh (≈ 7–14 kg).

**W′ (anaerobic work capacity) — for the alternative CP/W′ model**
- Bartram et al. 2018 (lab CP/W′, trained cyclists). PMC7560916: https://pmc.ncbi.nlm.nih.gov/articles/PMC7560916/
- → trained men W′ ≈ 12.7 ± 3.4 kJ, CP ≈ 301 ± 35 W; broader athlete range ~14–28 kJ.

> **Dropped after verification:** PMC10915604 (a 4-subject *triathlon* study — not a TT-cyclist threshold) and the Medical News Today / Harvard "calories-burned" basis for P_base/P_max (that is *metabolic* energy, ~4–5× the mechanical power at the pedals). Replace both with the studies above.
>
> The tuning constants (`hill_factor`, `fatigue_rate`, `recovery_rate`, `fatigue_impact`) are model choices, not externally sourced — justify them in the text, don't cite them.
