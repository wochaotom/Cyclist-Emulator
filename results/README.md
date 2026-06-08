# Results

Model outputs: the optimal pacing for each rider on each course, plus the two
sensitivity analyses. Everything here is generated from the model in
`../notebooks/model_v5.ipynb` and the inputs in `../data/` — nothing is hand-edited.

Courses are run at **one lap each** so the comparison is rider-vs-rider on identical
terrain. The real men's Tokyo is two laps; that 2-lap validation lives in the notebook.

## Files

| File | What it is |
|------|-----------|
| `sweep.py` | Runs the model for every rider × course, optimising pacing each time. Writes the table and plots below. |
| `sweep_results.csv` | Optimal finishing time (min) and the tuned `hill_factor` / `flat_boost` per rider × course. |
| `power_by_segment.csv` | Optimal average power on each course segment, per rider (the power-vs-position profile as a table). |
| `finish_times.png` | Bar chart of optimal finishing time by rider and course. |
| `speed_{tokyo,flanders,custom}.png` | Optimal speed vs distance, all riders. |
| `power_{tokyo,flanders,custom}.png` | Optimal power vs distance with the gradient profile shaded behind. |
| `wind_sensitivity.py` / `.csv` / `.png` | Finishing time vs a uniform head/tail wind offset (male_tt, 3 courses, calm-optimal pacing held fixed). |
| `power_deviation.py` / `.csv` / `.png` | Finishing time when the rider rides ±15% off the planned power (4 riders, Tokyo). |
| `verify_results.py` | Audit harness — re-checks all of the above for correctness, completeness, and that every required analysis is present. |

## Regenerate

```
python results/sweep.py
python results/wind_sensitivity.py
python results/power_deviation.py
```

## Audit

```
python results/verify_results.py
```

It re-loads the model, re-optimises every rider × course and checks the committed
numbers against it; checks data completeness and plausibility (speeds, rider ordering,
validation against the real 2021 winners); and checks the sensitivity outputs are
present and behave monotonically. It prints one PASS/FAIL line per check and the number
of failing checks last (0 = all pass).

## Headline numbers

- Optimal finishing times (1 lap): see `sweep_results.csv` / `finish_times.png`.
- Wind: Flanders is by far the most wind-exposed (~150 s per m/s of headwind), Tokyo ~70 s, the short custom loop ~16 s.
- Power deviation: riding 10% under the plan costs ~1.6–2.0 min on Tokyo; 10% over saves ~1.3–1.6 min.
