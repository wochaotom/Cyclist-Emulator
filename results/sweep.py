"""Run model_v5 across every rider profile and course, optimising pacing each time.

Reuses the real notebook code (notebooks/model_v5.ipynb) by executing its cells with the
rider/course/laps swapped in - no duplicated physics. Writes a finishing-time table
(results/sweep_results.csv), a per-segment optimal-power table (results/power_by_segment.csv),
a speed-vs-distance and a power-over-terrain plot per course, and a finishing-time bar chart
(results/finish_times.png).

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

# the four required riders - two types (TT specialist, climber) x two genders.
# `baseline` (the original generic rider) stays in rider_profiles.csv as a calibration reference, but is left out of the comparison.
riders = ["male_tt", "female_tt", "male_climber", "female_climber"]
courses = [("tokyo_olympic_tt.csv", "Tokyo"),
           ("flanders_world_tt.csv", "Flanders"),
           ("custom_5km_loop.csv", "Custom")]
rider_colors = {"male_tt": "#1f77b4", "female_tt": "#d62728",
                "male_climber": "#2ca02c", "female_climber": "#9467bd"}  # one colour per rider, used in every figure
OPT_STARTS = [[800, 50], [200, 10], [1500, 120], [1000, 80], [400, 30]]  # several starts - single-start under-converges on short/hilly courses

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
    res = min((minimize(sim, x0=s0, method="Nelder-Mead", bounds=[(0, 2000), (0, 150)]) for s0 in OPT_STARTS),
              key=lambda r: r.fun)  # best of several starts
    best_time = res.fun
    full = sim(tuple(res.x), True)  # t, fat, times, speeds, distances, drags, powers, fatigues, gradients
    distances, speeds, powers = full[4], full[3], full[6]
    course = ns["course"]  # the 1-lap course (list of segment tuples) for per-segment summaries
    return best_time, res.x, distances, speeds, powers, course

times = {}   # (rider, course) -> optimal seconds
params = {}  # (rider, course) -> (hill_factor, flat_boost)
speed_curves = {label: {} for _, label in courses}
power_curves = {label: {} for _, label in courses}  # (rider, course) -> (distances_m, powers_w)
seg_defs = {}  # label -> the course's 1-lap segment list (same for every rider)
for course_file, label in courses:
    for rider in riders:
        bt, x, dist, spd, pwr, course_segs = run(rider, course_file)
        times[(rider, label)] = bt
        params[(rider, label)] = x
        speed_curves[label][rider] = ([d / 1000 for d in dist], [s * 3.6 for s in spd])
        power_curves[label][rider] = (dist, pwr)  # raw metres + watts, for the P(x) profile
        seg_defs[label] = course_segs

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
        ax.plot(dk, sk, label=rider, color=rider_colors[rider], alpha=0.85)
    ax.set_title("Optimal speed vs distance - " + label + " (1 lap)")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Speed (km/h)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join("results", "speed_" + label.lower() + ".png"), dpi=90)

# Per-segment optimal power: the average power the rider holds on each stretch of road.
# A compact, readable table of the P(x) profile (the dense per-second curve is the plots below).
def segment_average_power(distances_m, powers_w, segments):
    """Bin the per-second power into course segments and return the mean power per segment."""
    bounds = []  # cumulative end-distance of each segment
    cum = 0.0
    for _name, d, _gr, _turn, _wind in segments:
        cum += d
        bounds.append(cum)
    sums = [0.0] * len(segments)
    counts = [0] * len(segments)
    si = 0
    for dd, pp in zip(distances_m, powers_w):
        while si < len(bounds) - 1 and dd > bounds[si]:  # advance to the segment this step falls in
            si += 1
        sums[si] += pp
        counts[si] += 1
    return [(sums[i] / counts[i]) if counts[i] else 0.0 for i in range(len(segments))]

with open(os.path.join("results", "power_by_segment.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rider", "course", "segment", "name", "start_km", "length_m", "grade_pct", "avg_power_w"])
    for label in labels:
        segments = seg_defs[label]
        for rider in riders:
            dist, pwr = power_curves[label][rider]
            avgs = segment_average_power(dist, pwr, segments)
            start = 0.0
            for i, (name, d, gr, turn, wind) in enumerate(segments):
                w.writerow([rider, label, i + 1, name, round(start / 1000, 2), round(d), gr, round(avgs[i])])
                start += d

for label in labels:
    segments = seg_defs[label]
    # gradient profile as a step series (km, grade %) to shade behind the power curves
    gd = []; gg = []
    cum = 0.0
    for name, d, gr, turn, wind in segments:
        gd.append(cum / 1000); gg.append(gr)
        cum += d
        gd.append(cum / 1000); gg.append(gr)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax2 = ax.twinx()  # terrain on its own axis, drawn behind the power lines
    ax2.fill_between(gd, gg, 0, color="0.85", zorder=0)
    ax2.set_ylabel("Gradient (%)")
    ax2.set_ylim(min(min(gg), -1), max(max(gg), 1) * 1.5)
    for rider in riders:
        dist, pwr = power_curves[label][rider]
        ax.plot([d / 1000 for d in dist], pwr, label=rider, color=rider_colors[rider], alpha=0.9, zorder=3)
    ax.set_zorder(ax2.get_zorder() + 1)  # bring the power lines in front of the terrain shading
    ax.patch.set_visible(False)          # but let the shading show through the (now transparent) power axes
    ax.set_title("Optimal power over terrain - " + label + " (1 lap)")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Power (W)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join("results", "power_" + label.lower() + ".png"), dpi=90)

# Finishing-time comparison: grouped bars, one group per course, one bar per rider.
fig, ax = plt.subplots(figsize=(10, 5))
bar_w = 0.8 / len(riders)
for ri, rider in enumerate(riders):
    xs = [ci + (ri - (len(riders) - 1) / 2) * bar_w for ci in range(len(labels))]
    ys = [times[(rider, label)] / 60 for label in labels]
    ax.bar(xs, ys, width=bar_w, label=rider, color=rider_colors[rider])
    for x, y in zip(xs, ys):  # value label above each bar, rotated to fit
        ax.text(x, y + 0.4, str(round(y, 1)), ha="center", va="bottom", fontsize=7, rotation=90)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels)
ax.set_ylabel("Finishing time (min)")
ax.set_ylim(0, max(times.values()) / 60 * 1.15)
ax.set_title("Optimal finishing time by rider and course (1 lap each)")
ax.grid(axis="y", alpha=0.3)
ax.legend(fontsize=8, ncol=len(riders), loc="upper center", bbox_to_anchor=(0.5, -0.08))
fig.tight_layout()
fig.savefig(os.path.join("results", "finish_times.png"), dpi=90)

print("wrote results/sweep_results.csv, results/power_by_segment.csv, and 7 plots")
