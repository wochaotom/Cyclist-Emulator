"""Wind sensitivity: how the optimal plan's finishing time changes with head/tail wind.

Wind enters the model only through the drag term, 0.5*rho*CdA*(v + w)^2, where w is the
per-segment effective headwind from the wind_map. This script optimises the pacing once
per course (calm conditions), then holds that plan fixed and shifts the headwind by a
uniform offset (negative = tailwind, positive = headwind), recording the finishing time
at each offset. Holding the plan fixed isolates the effect of wind (a real rider plans
once) and makes the response strictly monotonic - re-optimising at every offset instead
introduces optimiser noise that can make the curve wobble. It runs the TT specialist
(male_tt) on all three courses.

Note: the model uses a scalar, always-opposing headwind, so this measures sensitivity to
wind STRENGTH. Direction-dependent wind (a vector projected onto the rider's heading) is
a documented extension, not modelled here.

Writes results/wind_sensitivity.csv and results/wind_sensitivity.png.
Run from anywhere: python results/wind_sensitivity.py
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

RIDER = "male_tt"  # the TT specialist is the representative rider for the wind sweep
COURSES = [("tokyo_olympic_tt.csv", "Tokyo"),
           ("flanders_world_tt.csv", "Flanders"),
           ("custom_5km_loop.csv", "Custom")]
OFFSETS = [-4, -3, -2, -1, 0, 1, 2, 3, 4]  # m/s added to every segment's headwind (negative = tailwind)
COURSE_COLORS = {"Tokyo": "#1f77b4", "Flanders": "#d62728", "Custom": "#2ca02c"}

def build(course_file):
    """Exec the model's setup cells for male_tt on one course at one lap; return the namespace."""
    ns = {}
    for i in range(5):  # imports, constants, rider, course, simulate
        s = cells[i]
        if i == 2:
            s = s.replace('rider = "male_tt"', 'rider = "' + RIDER + '"')
        if i == 3:
            s = s.replace('course_file = "tokyo_olympic_tt.csv"', 'course_file = "' + course_file + '"')
            s = s.replace("laps = 2", "laps = 1")
        exec(compile(s, "cell" + str(i), "exec"), ns)
    return ns

def time_at(course_file, pacing, wind_offset):
    """Finishing minutes for a fixed pacing plan on a course at a uniform wind offset."""
    ns = build(course_file)
    ns["wind_map"] = {k: v + wind_offset for k, v in ns["wind_map"].items()}  # shift every exposure level
    return ns["simulate"](pacing) / 60

results = {label: {} for _, label in COURSES}
for course_file, label in COURSES:
    res = minimize(build(course_file)["simulate"], x0=[800, 50],
                   method="Nelder-Mead", bounds=[(0, 2000), (0, 150)])
    pacing = tuple(res.x)  # calm-optimal pacing, held fixed across all wind offsets
    for w in OFFSETS:
        results[label][w] = time_at(course_file, pacing, w)

with open(os.path.join("results", "wind_sensitivity.csv"), "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["rider", "course", "wind_offset_ms", "time_min", "delta_vs_calm_min"])
    for _, label in COURSES:
        calm = results[label][0]
        for w in OFFSETS:
            t = results[label][w]
            wr.writerow([RIDER, label, w, round(t, 2), round(t - calm, 2)])

# Plot the time change vs calm so all three courses are comparable on one axis.
fig, ax = plt.subplots(figsize=(9, 5))
print("Wind sensitivity (male_tt), minutes added vs calm:")
for _, label in COURSES:
    calm = results[label][0]
    deltas = [results[label][w] - calm for w in OFFSETS]
    ax.plot(OFFSETS, deltas, marker="o", label=label, color=COURSE_COLORS[label])
    span = results[label][4] - results[label][-4]  # +4 vs -4 m/s
    print("  " + label.ljust(9) + ": " + str(round(span, 1)) + " min across -4..+4 m/s ("
          + str(round(span * 60 / 8, 1)) + " s per m/s)")
ax.axvline(0, color="0.6", linewidth=0.8)
ax.axhline(0, color="0.6", linewidth=0.8)
ax.set_xlabel("Headwind offset (m/s)   (negative = tailwind)")
ax.set_ylabel("Finishing time change vs calm (min)")
ax.set_title("Wind sensitivity - male_tt, calm-optimal pacing held fixed")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join("results", "wind_sensitivity.png"), dpi=90)
print("wrote results/wind_sensitivity.csv and results/wind_sensitivity.png")
