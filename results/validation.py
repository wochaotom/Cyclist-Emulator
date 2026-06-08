"""Validation: the optimised model vs the real 2021 ITT winners.

Runs each rider at the real race configuration (correct course and lap count), optimises
the pacing, and compares the finishing time to the actual winner. The TT specialist is the
right comparison because real ITT winners are specialists/rouleurs.

Comparable races (women's Flanders is omitted - it is a different, shorter 30.3 km course
we do not carry a CSV for):
  - men's Tokyo, 2 laps (44.2 km)   vs Primoz Roglic
  - women's Tokyo, 1 lap (22.1 km)  vs Annemiek van Vleuten
  - men's Flanders, 43.3 km         vs Filippo Ganna

Real times are from data/real_results.csv. Writes results/validation.csv and
results/validation.png. Run from anywhere: python results/validation.py
"""
import json, os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

nb = json.load(open(os.path.join("notebooks", "model_v5.ipynb"), encoding="utf-8-sig"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]

# real winner times (seconds) from data/real_results.csv - keep the FASTEST (winner) per race
real = {}
for r in csv.DictReader(open(os.path.join("data", "real_results.csv"))):
    key = (r["course"], r["gender"], round(float(r["distance_km"])))
    t = float(r["time_s"])
    if key not in real or t < real[key][1]:  # smallest time = winner
        real[key] = (r["rider"], t)

# (label, rider, course_file, laps, real key)
TARGETS = [
    ("Tokyo men (2 laps)",  "male_tt",   "tokyo_olympic_tt.csv", 2, ("tokyo_2021", "M", 44)),
    ("Tokyo women (1 lap)", "female_tt", "tokyo_olympic_tt.csv", 1, ("tokyo_2021", "F", 22)),
    ("Flanders men",        "male_tt",   "flanders_world_tt.csv", 1, ("flanders_2021", "M", 43)),
]
OPT_STARTS = [[800, 50], [200, 10], [1500, 120], [1000, 80], [400, 30]]  # multi-start optimiser (matches sweep.py)

def build(rider, course_file, laps):
    """Exec the model's setup cells for one rider/course/lap-count; return the namespace."""
    ns = {}
    for i in range(5):  # imports, constants, rider, course, simulate
        s = cells[i]
        if i == 2:
            s = s.replace('rider = "male_tt"', 'rider = "' + rider + '"')
        if i == 3:
            s = s.replace('course_file = "tokyo_olympic_tt.csv"', 'course_file = "' + course_file + '"')
            s = s.replace("laps = 2", "laps = " + str(laps))
        exec(compile(s, "cell" + str(i), "exec"), ns)
    return ns

rows = []
for label, rider, course_file, laps, key in TARGETS:
    ns = build(rider, course_file, laps)
    res = min((minimize(ns["simulate"], x0=s0, method="Nelder-Mead", bounds=[(0, 2000), (0, 150)]) for s0 in OPT_STARTS),
              key=lambda r: r.fun)
    model_min = res.fun / 60
    winner, real_s = real[key]
    real_min = real_s / 60
    err = (model_min - real_min) / real_min * 100
    km = sum(d for _, d, *_ in ns["course"]) / 1000  # total course distance actually simulated
    rows.append((label, rider, winner, round(km, 1), round(model_min, 2), round(real_min, 2), round(err, 1)))

with open(os.path.join("results", "validation.csv"), "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["race", "rider", "real_winner", "distance_km", "model_min", "real_min", "error_pct"])
    wr.writerows(rows)

print("Model vs real 2021 ITT winners:")
print("race".ljust(22) + "model".ljust(9) + "real".ljust(9) + "error")
for label, rider, winner, km, model_min, real_min, err in rows:
    print(label.ljust(22) + (str(model_min) + " min").ljust(9) + (str(real_min) + " min").ljust(9)
          + ("+" if err >= 0 else "") + str(err) + "%  (vs " + winner + ")")

# Grouped bar: model vs real per race, with the error printed above each pair.
fig, ax = plt.subplots(figsize=(9, 5))
x = range(len(rows))
ax.bar([i - 0.2 for i in x], [r[4] for r in rows], width=0.4, label="model (optimal)", color="#1f77b4")
ax.bar([i + 0.2 for i in x], [r[5] for r in rows], width=0.4, label="real winner", color="#7f7f7f")
for i, r in enumerate(rows):
    ax.text(i, max(r[4], r[5]) + 1, ("+" if r[6] >= 0 else "") + str(r[6]) + "%", ha="center", fontsize=9)
ax.set_xticks(list(x))
ax.set_xticklabels([r[0] for r in rows], fontsize=9)
ax.set_ylabel("Finishing time (min)")
ax.set_ylim(0, max(max(r[4], r[5]) for r in rows) * 1.15)
ax.set_title("Model vs real 2021 ITT winners")
ax.grid(axis="y", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join("results", "validation.png"), dpi=90)
print("wrote results/validation.csv and results/validation.png")
