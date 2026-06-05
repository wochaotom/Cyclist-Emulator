# References

Deduped source list behind the course data and the model's parameters — ready to format into the paper's reference section. (`data-sources.md` has the same links with more context.)

## Courses, routes, and race results

**2021 Tokyo Olympic ITT** — Fuji Speedway (men 44.2 km / 2 laps, women 22.1 km / 1 lap)
- Best elevation breakdown (real elevations + segment distances): NBC Olympics course page: https://www.nbcolympics.com/news/cycling-101-courses → per lap: descent to 455 m, main climb 5.4 km to 676 m (**≈4.1% avg**), descent, 2.0 km climb to pit lane (**≈6.8%**), final 2.1 km climb to finish.
- In-circuit ramp: VeloViewer "Fuji Speedway Climb", 0.86 km / 53 m / **4.4%**: https://veloviewer.com/segments/16466365
- Route narrative: UCI https://www.uci.org/article/olympic-gold-awaits-at-the-foot-of-mount-fuji/55jtcCLEgwlDZr0WXhDvcv ; cyclingstage https://www.cyclingstage.com/summer-olympics-2021/route-itt-tokyo-2021/
- Results (official host, JS-rendered — cross-check vs Wikipedia/UCI): olympics.com men https://www.olympics.com/en/olympic-games/tokyo-2020/results/cycling-road/men-s-individual-time-trial , women https://www.olympics.com/en/olympic-games/tokyo-2020/results/cycling-road/women-s-individual-time-trial . Roglič 55:04.19; van Vleuten 30:13.49.
- *Caveat:* the "8.9% / 5.9% / 4% / 11%" pitch figures are Cyclingnews **preview prose**, not an official profile; "11%" is unverified, and there is **no public official Tokyo-TT technical guide or GPX**. Men's gain is quoted as both 846 m and ~900 m (±50 m). Do **not** reuse the VeloViewer/PJAMM "Fuji" climbs — those are the road race, not the TT.

**2021 UCI Worlds ITT** — Knokke-Heist → Bruges (men 43.3 km, women 30.3 km)
- Official course + elevation: UCI Technical Guide (PDF, open): https://downloads.ctfassets.net/761l7gh5x5an/lYf25TYStUnbzj6vRXM7f/00f43906c8264b99813bed9102d8bc45/guide-tech-cdmr-flandres-2021-eng-web-md.pdf — pan-flat (~78 m men / ~54 m women). Official GPX via flanders2021.com / Knokke-Heist Strava: https://www.flanders2021.com/en/ride-knokke-heist-brugge
- Route description: cyclingstage https://www.cyclingstage.com/world-championships-2021-flanders/route-itt-wc-2021/
- Results: Cyclingnews men https://www.cyclingnews.com/races/uci-road-world-championships-2021/men-elite-individual-time-trial/results/ , women https://www.cyclingnews.com/races/uci-road-world-championships-2021/women-elite-individual-time-trial/results/ . Ganna 47:47; van Dijk ~36:05.

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

**Air density (ρ)**
- International Standard Atmosphere — dry air, 15 °C at sea level: 1.225 kg/m³.
- → treated as constant per course; a few percent lower at Fuji's ~600 m, assumed negligible.

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
