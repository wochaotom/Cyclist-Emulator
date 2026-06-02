# Paper (LaTeX source)

`main.tex` is the scaffold for the write-up. Paste it into Overleaf — or sync this folder with Overleaf via its GitHub integration — and write the prose there.

**Already filled in:** the section structure, the model equations, the variable table, the results tables (numbers reproduced from `src/`), and the assumptions and known-limitations lists.

**Marked `% TODO (write yourselves)`:** the summary sheet, background, problem restatement, all interpretation of the results, the justification of each assumption, the model-assessment discussion, and the conclusion. These are the graded reasoning — write them in your own words, because you can be asked to defend any of it in the consultations.

**Figures:** `python src/plots.py` regenerates the four figures into `figures/` (needs `matplotlib`). They are referenced by `main.tex` and recompute from the current model, so re-run it if the parameters or courses change.
