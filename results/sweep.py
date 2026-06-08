"""Run model_v5 across every rider profile and course, optimising pacing each time.

Reuses the real notebook code (notebooks/model_v5.ipynb) by executing its cells with the
rider/course/laps swapped in - no duplicated physics. Writes a finishing-time table
(results/sweep_results.csv) and one optimal-speed-vs-distance plot per course.

Courses are held at one lap each so the comparison is rider-vs-rider on identical terrain
(the real men's Tokyo is two laps - that 2-lap validation is in model_v5 itself).

Run from anywhere: python results/sweep.py
"""
import json, os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
os.makedirs("results", exist_ok=True)

nb = json.load(open(os.path.join("notebooks", "model_v5.ipynb"), encoding="utf-8-sig"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
# cells: 0 imports, 1 world constants, 2 rider, 3 course, 4 simulate, 5 optimiser, 6 plots

riders = ["baseline", "male_tt", "female_tt", "male_climber", "female_climber"]
courses = [("tokyo_olympic_tt.csv", "Tokyo"),
           ("flanders_world_tt.csv", "Flanders"),
           ("custom_5km_loop.csv", "Custom")]

def run(rider, course_file):
    """Execute the notebook's setup cells for one rider/course, then optimise the pacing."""
    ns = {}
    for i in range(5):  # imports, constants, rider, course, simulate
        s = cells[i]
        if i == 2:
            s = s.replace('rider = "male_tt"', 'rider = "' + rider + '"')
        if i == 3:
            s = s.replace('course_file = "tokyo_olympic_tt.csv"', 'course_file = "' + course_file + '"')
            s = s.replace("laps = 2", "laps = 1")  # one lap per course for an apples-to-apples comparison
        exec(compile(s, "cell" + str(i), "exec"), ns)
    sim = ns["simulate"]  # the real simulate() from the notebook
    res = minimize(sim, x0=[800, 50], method="Nelder-Mead", bounds=[(0, 2000), (0, 150)])
    best_time = res.fun
    full = sim(tuple(res.x), True)  # t, fat, times, speeds, distances, drags, powers, fatigues, gradients
    distances, speeds = full[4], full[3]
    return best_time, res.x, distances, speeds

times = {}   # (rider, course) -> optimal seconds
params = {}  # (rider, course) -> (hill_factor, flat_boost)
speed_curves = {label: {} for _, label in courses}
for course_file, label in courses:
    for rider in riders:
        bt, x, dist, spd = run(rider, course_file)
        times[(rider, label)] = bt
        params[(rider, label)] = x
        speed_curves[label][rider] = ([d / 1000 for d in dist], [s * 3.6 for s in spd])

labels = [label for _, label in courses]
print("Optimal finishing time (min) by rider x course (1 lap each):")
print("rider".ljust(16) + "".join(l.ljust(12) for l in labels))
with open(os.path.join("results", "sweep_results.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rider"] + [l + "_min" for l in labels] +
               [l + "_hill_factor" for l in labels] + [l + "_flat_boost" for l in labels])
    for rider in riders:
        mins = [round(times[(rider, l)] / 60, 1) for l in labels]
        hf = [round(params[(rider, l)][0]) for l in labels]
        fb = [round(params[(rider, l)][1]) for l in labels]
        print(rider.ljust(16) + "".join((str(m) + " min").ljust(12) for m in mins))
        w.writerow([rider] + mins + hf + fb)

for label in labels:
    fig, ax = plt.subplots(figsize=(9, 4))
    for rider in riders:
        dk, sk = speed_curves[label][rider]
        ax.plot(dk, sk, label=rider, alpha=0.85)
    ax.set_title("Optimal speed vs distance - " + label + " (1 lap)")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Speed (km/h)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join("results", "sweep_" + label.lower() + ".png"), dpi=90)

print("wrote results/sweep_results.csv and 3 plots")
