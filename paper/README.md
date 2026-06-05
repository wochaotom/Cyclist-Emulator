# Paper (LaTeX source)

`main.tex` is the LaTeX scaffold for the write-up: the section structure for the M142 rubric (summary, introduction, model, results, assessment, conclusion, references), with `% TODO (write yourselves)` markers on the graded prose. Paste it into Overleaf — or sync this folder via Overleaf's GitHub integration — and write there.

## Important: the model content is from the retired model

The equations, the variable table (CP, W′), the assumptions list, and every results table and figure in `main.tex` describe the archived **critical-power (CP/W′)** model in [`../archive/cp_w_prime_model/`](../archive/cp_w_prime_model/) — **not** the canonical notebook ([`../notebooks/model_v3.ipynb`](../notebooks/model_v3.ipynb)). Before submission the model section and results must be redone for the canonical model:

- Replace the steady-state power-balance equation and the CP/W′ pacing description with the notebook's time-stepping force balance and power-threshold fatigue (see the "Model" section of the main [`../README.md`](../README.md)).
- Swap the CP/W′ variable rows for the notebook's parameters (`P_base`, `P_threshold`, `P_max`, `hill_factor`, the fatigue constants).
- Re-run the rider × course, wind, and power-deviation analyses on the notebook and replace the tables with those numbers.

## Figures

The four `figures/*.png` referenced by `main.tex` were CP/W′ outputs and have been removed, so the file will not compile until they are regenerated. Produce the equivalents from the canonical notebook and add them back.

Treat `main.tex` as a structural skeleton only. The CP/W′ model survives in the paper solely as the rubric's required "alternative modeling choice."
