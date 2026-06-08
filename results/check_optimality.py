"""Optimality check: are the sweep's optimal times actually the global optimum?

sweep.py optimises pacing with a single Nelder-Mead run from one start point. On a
flat objective that can under-converge (it is what made the early wind sweep wobble).
This script re-optimises every rider x course from several different start points and
reports the best time found against the committed sweep time. If the committed time is
within 0.1 min of the best-of-many-starts everywhere, the sweep optima are robust.

Writes results/optimality.csv and prints a verdict. Read-only on the other results.
Run from anywhere: python results/check_optimality.py
"""
import json, os, csv
from scipy.optimize import minimize

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

nb = json.load(open(os.path.join("notebooks", "model_v5.ipynb"), encoding="utf-8-sig"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]

RIDERS = ["male_tt", "female_tt", "male_climber", "female_climber"]
COURSES = [("tokyo_olympic_tt.csv", "Tokyo"),
           ("flanders_world_tt.csv", "Flanders"),
           ("custom_5km_loop.csv", "Custom")]
STARTS = [[800, 50], [200, 10], [1500, 120], [1000, 80], [400, 30]]  # spread of Nelder-Mead start points

sweep = {r["rider"]: r for r in csv.DictReader(open(os.path.join("results", "sweep_results.csv")))}

def build(rider, course_file):
    ns = {}
    for i in range(5):  # imports, constants, rider, course, simulate
        s = cells[i]
        if i == 2:
            s = s.replace('rider = "male_tt"', 'rider = "' + rider + '"')
        if i == 3:
            s = s.replace('course_file = "tokyo_olympic_tt.csv"', 'course_file = "' + course_file + '"')
            s = s.replace("laps = 2", "laps = 1")
        exec(compile(s, "cell" + str(i), "exec"), ns)
    return ns

rows = []
worst = 0.0
for course_file, label in COURSES:
    for rider in RIDERS:
        sim = build(rider, course_file)["simulate"]
        best = min(minimize(sim, x0=s0, method="Nelder-Mead", bounds=[(0, 2000), (0, 150)]).fun
                   for s0 in STARTS) / 60
        committed = float(sweep[rider][label + "_min"])
        improvement = committed - best  # positive means multi-start found a faster time
        worst = max(worst, improvement)
        rows.append((rider, label, round(committed, 2), round(best, 2), round(improvement, 2)))

with open(os.path.join("results", "optimality.csv"), "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["rider", "course", "committed_min", "best_multistart_min", "improvement_min"])
    wr.writerows(rows)

print("Optimality check (" + str(len(STARTS)) + " start points per rider x course):")
print("rider".ljust(16) + "course".ljust(10) + "committed".ljust(11) + "best".ljust(9) + "gain")
for rider, label, committed, best, improvement in rows:
    flag = "   <-- sub-optimal" if improvement > 0.1 else ""
    print(rider.ljust(16) + label.ljust(10) + (str(committed) + " min").ljust(11)
          + (str(best) + " min").ljust(9) + str(improvement) + flag)
print()
if worst <= 0.1:
    print("VERDICT: sweep optima are robust - within 0.1 min of the best of "
          + str(len(STARTS)) + " starts everywhere (max gain " + str(round(worst, 2)) + " min).")
else:
    print("VERDICT: multi-start beats the committed sweep by up to " + str(round(worst, 2))
          + " min - sweep.py should use multi-start.")
print("wrote results/optimality.csv")
