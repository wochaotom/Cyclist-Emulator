"""Generate the figures for the paper into paper/figures/.

Run:  python src/plots.py
Needs matplotlib (pip install matplotlib). Everything is computed live from the
model, so the figures always match the current parameters and courses.
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")            # render to files, no display needed
import matplotlib.pyplot as plt

from course import load_course
from pacing import simulate_pacing, spend_on_slow_segments
from parameters import DEFAULT_PHYSICS, RIDER_PROFILES

HERE = os.path.dirname(__file__)
COURSES = os.path.join(HERE, "..", "data", "courses")
FIGDIR = os.path.join(HERE, "..", "paper", "figures")
PHYS = DEFAULT_PHYSICS


def rider(name):
    """Total mass (rider + bike), CP, and W' for a named rider profile."""
    r = RIDER_PROFILES[name]
    return r["rider_mass"] + PHYS["bike_mass"], r["cp"], r["w_prime"]


def paced(course, name, wind_offset=0.0):
    """Run a rider's paced ride on a course; returns (rows, total_time, feasible)."""
    mass, cp, wp = rider(name)
    plan = spend_on_slow_segments(course, mass, PHYS, cp, wp)
    return simulate_pacing(course, plan, mass, PHYS, cp, wp, wind_offset)


def fig_pacing_profile():
    """Figure: speed and remaining W' reserve along the custom loop."""
    course = load_course(os.path.join(COURSES, "custom_5km_loop.csv"))
    rows, _, _ = paced(course, "male_tt")
    x, speed, reserve = [], [], []
    for seg, power, spd, t, res in rows:
        x += [seg.start_m / 1000, seg.end_m / 1000]
        speed += [spd, spd]
        reserve += [res / 1000, res / 1000]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
    ax1.plot(x, speed)
    ax1.set_ylabel("Speed (m/s)")
    ax1.set_title("Paced ride: male TT specialist, custom loop")
    ax1.grid(alpha=0.3)
    ax2.plot(x, reserve, color="tab:red")
    ax2.set_ylabel("W' reserve (kJ)")
    ax2.set_xlabel("Distance (km)")
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "pacing_profile.png"), dpi=150)
    plt.close(fig)


def fig_crossover():
    """Figure: climber minus TT-specialist finishing time for each course."""
    courses = {name: load_course(os.path.join(COURSES, f))
               for name, f in [("Custom", "custom_5km_loop.csv"),
                               ("Tokyo", "tokyo_olympic_tt.csv"),
                               ("Flanders", "flanders_world_tt.csv")]}
    male = [paced(c, "male_climber")[1] - paced(c, "male_tt")[1] for c in courses.values()]
    female = [paced(c, "female_climber")[1] - paced(c, "female_tt")[1] for c in courses.values()]

    x = list(range(len(courses)))
    w = 0.35
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([i - w / 2 for i in x], male, w, label="male")
    ax.bar([i + w / 2 for i in x], female, w, label="female")
    ax.axhline(0, color="k", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(list(courses))
    ax.set_ylabel("Climber - TT time (s)")
    ax.set_title("Rider x course: negative means the climber is faster")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "crossover.png"), dpi=150)
    plt.close(fig)


def fig_wind():
    """Figure: finish time vs a uniform wind offset."""
    course = load_course(os.path.join(COURSES, "custom_5km_loop.csv"))
    offsets = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
    times = [paced(course, "male_tt", off)[1] for off in offsets]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(offsets, times, marker="o")
    ax.axvline(0, color="k", linewidth=0.8, linestyle=":")
    ax.set_xlabel("Wind offset (m/s):  + headwind,  - tailwind")
    ax.set_ylabel("Finish time (s)")
    ax.set_title("Wind sensitivity: male TT specialist, custom loop")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "wind_sensitivity.png"), dpi=150)
    plt.close(fig)


def fig_validation():
    """Figure: model time vs the real 2021 men's winners."""
    # fastest man on each real course, from the results file
    real = {}
    with open(os.path.join(HERE, "..", "data", "real_results.csv"), newline="") as f:
        for row in csv.DictReader(f):
            if row["gender"] != "M":
                continue
            key, t = row["course"], float(row["time_s"])
            if key not in real or t < real[key][1]:
                real[key] = (row["rider"], t)

    tokyo = load_course(os.path.join(COURSES, "tokyo_olympic_tt.csv"))
    flanders = load_course(os.path.join(COURSES, "flanders_world_tt.csv"))
    model = {"tokyo_2021": paced(tokyo + tokyo, "male_tt")[1],   # men ride 2 laps
             "flanders_2021": paced(flanders, "male_tt")[1]}

    keys = ["tokyo_2021", "flanders_2021"]
    labels = [f"Tokyo\n({real[k][0]})" for k in keys[:1]] + [f"Flanders\n({real['flanders_2021'][0]})"]
    model_t = [model[k] for k in keys]
    real_t = [real[k][1] for k in keys]

    x = list(range(len(keys)))
    w = 0.35
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([i - w / 2 for i in x], model_t, w, label="model (male TT archetype)")
    ax.bar([i + w / 2 for i in x], real_t, w, label="real winner")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Finish time (s)")
    ax.set_title("Validation: model vs 2021 winners (men)")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "validation.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(FIGDIR, exist_ok=True)
    fig_pacing_profile()
    fig_crossover()
    fig_wind()
    fig_validation()
    print("figures written to paper/figures/")
