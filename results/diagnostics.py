"""Per-rider diagnostic 5-panels, the optimization heatmap, and a parameter-sensitivity table.

Reuses model_v5 (no duplicated physics). For each rider on Tokyo at its real race
config (men two laps, women one), plots optimal-vs-baseline gradient/speed/power/
fatigue/drag (diag_<rider>.png). Also writes the (hill_factor, flat_boost) completion-
time heatmap with 1-D slices (heatmap_tokyo.png) and a one-at-a-time +/-10% sensitivity
table over threshold power, CdA and mass (param_sensitivity.csv).

Run from anywhere: python results/diagnostics.py
"""
import json, os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(REPO, "results")
nb = json.load(open(os.path.join(REPO, "notebooks", "model_v5.ipynb"), encoding="utf-8-sig"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
STARTS = [[800, 50], [200, 10], [1500, 120], [1000, 80], [400, 30]]  # multi-start (matches sweep.py)

def build(rider, cf, laps):
    ns = {}
    for i in range(5):
        s = cells[i]
        if i == 2: s = s.replace('rider = "male_tt"', 'rider = "%s"' % rider)
        if i == 3:
            s = s.replace('course_file = "tokyo_olympic_tt.csv"', 'course_file = "%s"' % cf)
            s = s.replace("laps = 2", "laps = %d" % laps)
        exec(compile(s, "c%d" % i, "exec"), ns)
    return ns

def opt(sim):
    return min((minimize(sim, x0=s, method="Nelder-Mead", bounds=[(0, 2000), (0, 150)]) for s in STARTS), key=lambda r: r.fun)

NICE = {"male_tt": "Male TT specialist", "female_tt": "Female TT specialist",
        "male_climber": "Male climber", "female_climber": "Female climber"}
CF = "tokyo_olympic_tt.csv"

for rider, laps in [("male_tt", 2), ("female_tt", 1), ("male_climber", 2), ("female_climber", 1)]:
    ns = build(rider, CF, laps); sim = ns["simulate"]; Pthr = ns["P_threshold"]
    r = opt(sim); hf, fb = r.x; topt = r.fun / 60; tbase = sim((800, 0)) / 60
    o = sim((hf, fb), True); b = sim((800, 0), True)  # t,fat,times,speeds,distances,drags,powers,fatigues,gradients
    fig, ax = plt.subplots(5, 1, figsize=(9, 11))
    fig.suptitle("%s - Tokyo (%d lap%s): optimal %.1f min vs baseline %.1f min" % (NICE[rider], laps, "s" if laps > 1 else "", topt, tbase), fontsize=11, y=0.995)
    ax[0].plot([d / 1000 for d in b[4]], b[8], color="0.4"); ax[0].set_ylabel("Gradient (%)"); ax[0].set_xlabel("Distance (km)"); ax[0].grid(alpha=0.3)
    ax[1].plot(b[2], [s * 3.6 for s in b[3]], label="baseline", color="#1f77b4"); ax[1].plot(o[2], [s * 3.6 for s in o[3]], label="optimal", color="#d62728"); ax[1].set_ylabel("Speed (km/h)"); ax[1].set_xlabel("Time (s)"); ax[1].grid(alpha=0.3); ax[1].legend(fontsize=8)
    ax[2].plot(b[2], b[6], color="#1f77b4"); ax[2].plot(o[2], o[6], color="#d62728"); ax[2].axhline(Pthr, color="0.5", ls="--", lw=0.8, label="P_threshold"); ax[2].set_ylabel("Power (W)"); ax[2].set_xlabel("Time (s)"); ax[2].grid(alpha=0.3); ax[2].legend(fontsize=8)
    ax[3].plot(b[2], b[7], color="#1f77b4"); ax[3].plot(o[2], o[7], color="#d62728"); ax[3].set_ylabel("Fatigue (0-1)"); ax[3].set_xlabel("Time (s)"); ax[3].grid(alpha=0.3)
    ax[4].plot(b[2], b[5], color="#1f77b4"); ax[4].plot(o[2], o[5], color="#d62728"); ax[4].set_ylabel("Drag (N)"); ax[4].set_xlabel("Time (s)"); ax[4].grid(alpha=0.3)
    fig.tight_layout(rect=[0, 0, 1, 0.98]); fig.savefig(os.path.join(RES, "diag_%s.png" % rider), dpi=90); plt.close(fig)
    print("diag", rider, "opt", round(topt, 1), "base", round(tbase, 1))

# optimization heatmap + 1-D slices, male_tt Tokyo 2 laps
ns = build("male_tt", CF, 2); sim = ns["simulate"]; r = opt(sim); ohf, ofb = r.x
H = np.linspace(0, 2000, 28); Fb = np.linspace(0, 150, 28)
Z = np.array([[sim((h, f)) / 60 for h in H] for f in Fb])
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
c = ax[0].contourf(H, Fb, Z, levels=22, cmap="viridis"); ax[0].contour(H, Fb, Z, levels=11, colors="white", linewidths=0.3, alpha=0.5)
ax[0].plot(ohf, ofb, "r*", ms=16, label="optimum (%.0f, %.0f)" % (ohf, ofb)); ax[0].set_xlabel("hill_factor"); ax[0].set_ylabel("flat_boost (W)"); ax[0].set_title("Completion time (min) over the two pacing parameters"); ax[0].legend(loc="upper right", fontsize=8); fig.colorbar(c, ax=ax[0], label="time (min)")
Hs = np.linspace(0, 2000, 60); Fs = np.linspace(0, 150, 60)
ax[1].plot(Hs, [sim((h, ofb)) / 60 for h in Hs], label="vary hill_factor", color="#1f77b4")
ax2 = ax[1].twiny(); ax2.plot(Fs, [sim((ohf, f)) / 60 for f in Fs], label="vary flat_boost", color="#d62728")
ax[1].set_xlabel("hill_factor"); ax2.set_xlabel("flat_boost (W)"); ax[1].set_ylabel("completion time (min)"); ax[1].set_title("1-D slices through the optimum"); ax[1].grid(alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(RES, "heatmap_tokyo.png"), dpi=90); plt.close(fig)
print("heatmap opt", round(ohf), round(ofb))

# parameter sensitivity, male_tt Tokyo 2 laps
def time_with(param, factor):
    ns = build("male_tt", CF, 2); ns[param] *= factor
    return opt(ns["simulate"]).fun / 60
rows = []
for label, param in [("Threshold power", "P_threshold"), ("Drag area CdA", "CdA"), ("Total mass", "m")]:
    rows.append((label, round(time_with(param, 0.9), 1), round(time_with(param, 1.0), 1), round(time_with(param, 1.1), 1)))
    print(rows[-1])
with open(os.path.join(RES, "param_sensitivity.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["parameter", "minus10pct_min", "baseline_min", "plus10pct_min"]); w.writerows(rows)
print("DONE")
