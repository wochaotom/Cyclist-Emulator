# CP/W′ model (retired)

An earlier model of the project, on a **critical-power (CP / W′)** framework: a rider holds critical power CP for a long time and spends a finite anaerobic reserve W′, with pacing chosen to spend the reserve on the slowest segments. It also includes wind and power-deviation sensitivity analyses, a rider × course comparison, and a validation against the 2021 winners.

It has been **retired as the canonical model** in favour of the dynamic, time-stepping model in [`../../notebooks/model_v3.ipynb`](../../notebooks/model_v3.ipynb). It is kept here as:

- the **alternative modeling choice** the rubric asks the paper to discuss (a different fatigue framework), and
- part of the project's documented history.

To run it (standard library only): `python simulate.py`, `python compare.py`, `python sensitivity.py`, or `python plots.py` from inside this folder.
