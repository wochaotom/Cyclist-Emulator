"""Power-deviation sensitivity: the time cost of not hitting the planned power.

A rider cannot execute a pacing plan perfectly. This script takes each rider's
OPTIMAL pacing on Tokyo and asks: if they ride at (1 + d) times the plan everywhere
- d from -15% to +15% - how does the finishing time change?

A uniform power scale s is applied consistently: P_base, P_max and P_threshold are
all multiplied by s and the pacing knobs (hill_factor, flat_boost) by s. Because the
fatigue term depends only on the ratio P_out / P_threshold, that ratio is unchanged,
so this is a clean "same plan, scaled effort" experiment. At s = 1 it reproduces the
optimal time (printed as a self-check). Runs all four riders on Tokyo (1 lap).

Writes results/power_deviation.csv and results/power_deviation.png.
Run from anywhere: python results/power_deviation.py
"""
import json, os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

nb = json.load(open(os.path.join("notebooks", "model_v5.ipynb"), encoding="utf-8-sig"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]

RIDERS = ["male_tt", "female_tt", "male_climber", "female_climber"]
RIDER_COLORS = {"male_tt": "#1f77b4", "female_tt": "#d62728",
                "male_climber": "#2ca02c", "female_climber": "#9467bd"}
DEVIATIONS = [-15, -10, -5, 0, 5, 10, 15]  # percent off the planned power
COURSE_FILE, COURSE = "tokyo_olympic_tt.csv", "Tokyo"

# optimal pacing knobs per rider (from the committed sweep)
sweep = {}
with open(os.path.join("results", "sweep_results.csv"), newline="") as f:
    for row in csv.DictReader(f):
        sweep[row["rider"]] = row

def time_at_scale(rider, s):
    """Finishing minutes for `rider` on Tokyo riding at s times the optimal power plan."""
    ns = {}
    for i in range(5):  # imports, constants, rider, course, simulate
        src = cells[i]
        if i == 2:
            src = src.replace('rider = "male_tt"', 'rider = "' + rider + '"')
        if i == 3:
            src = src.replace('course_file = "tokyo_olympic_tt.csv"', 'course_file = "' + COURSE_FILE + '"')
            src = src.replace("laps = 2", "laps = 1")
        exec(compile(src, "cell" + str(i), "exec"), ns)
    ns["P_base"] *= s          # scale the whole power profile by s...
    ns["P_max"] *= s
    ns["P_threshold"] *= s     # ...threshold too, so the fatigue ratio is unchanged
    hf = float(sweep[rider][COURSE + "_hill_factor"]) * s
    fb = float(sweep[rider][COURSE + "_flat_boost"]) * s
    return ns["simulate"]((hf, fb)) / 60

results = {rider: {d: time_at_scale(rider, 1 + d / 100) for d in DEVIATIONS} for rider in RIDERS}

with open(os.path.join("results", "power_deviation.csv"), "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["rider", "course", "deviation_pct", "time_min", "delta_vs_optimal_min"])
    for rider in RIDERS:
        opt = results[rider][0]
        for d in DEVIATIONS:
            t = results[rider][d]
            wr.writerow([rider, COURSE, d, round(t, 2), round(t - opt, 2)])

# self-check: at 0% deviation the time should equal the committed optimum
print("Self-check (0% deviation should match sweep_results Tokyo_min):")
for rider in RIDERS:
    print("  " + rider.ljust(15) + " model " + str(round(results[rider][0], 1))
          + " vs sweep " + sweep[rider]["Tokyo_min"])

fig, ax = plt.subplots(figsize=(9, 5))
print("Time cost of mis-pacing (min vs optimal):")
for rider in RIDERS:
    opt = results[rider][0]
    deltas = [results[rider][d] - opt for d in DEVIATIONS]
    ax.plot(DEVIATIONS, deltas, marker="o", label=rider, color=RIDER_COLORS[rider])
    print("  " + rider.ljust(15) + " -10%: +" + str(round(results[rider][-10] - opt, 1))
          + " min   +10%: " + str(round(results[rider][10] - opt, 1)) + " min")
ax.axvline(0, color="0.6", linewidth=0.8)
ax.axhline(0, color="0.6", linewidth=0.8)
ax.set_xlabel("Power deviation from plan (%)   (negative = under-power)")
ax.set_ylabel("Finishing time change vs optimal (min)")
ax.set_title("Power-deviation sensitivity - Tokyo (1 lap)")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join("results", "power_deviation.png"), dpi=90)
print("wrote results/power_deviation.csv and results/power_deviation.png")
