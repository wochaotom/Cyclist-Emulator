"""Sensitivity analyses required by the problem: how the finishing time responds
to (1) wind and (2) the rider missing the target power.

Both take the paced plan (spend the reserve on the slow sections) and re-run it under a
perturbation, answering "if conditions or execution differ from the plan, how
much does the time move?"
"""

import os

from course import load_course
from pacing import simulate_pacing, spend_on_slow_segments
from parameters import DEFAULT_PHYSICS, RIDER_PROFILES


def wind_sensitivity(course, mass, phys, cp, w_prime, offsets):
    """Finish time vs a uniform wind offset (m/s; + headwind, - tailwind)."""
    plan = spend_on_slow_segments(course, mass, phys, cp, w_prime)
    rows = []
    for off in offsets:
        _, total, feasible = simulate_pacing(course, plan, mass, phys, cp, w_prime, off)
        rows.append((off, total, feasible))
    return rows


def power_deviation_sensitivity(course, mass, phys, cp, w_prime, deviations):
    """Finish time when the rider holds (1 + dev) x the planned power everywhere."""
    plan = spend_on_slow_segments(course, mass, phys, cp, w_prime)
    rows = []
    for dev in deviations:
        powers = [p * (1 + dev) for p in plan]
        _, total, feasible = simulate_pacing(course, powers, mass, phys, cp, w_prime)
        rows.append((dev, total, feasible))
    return rows


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    course = load_course(os.path.join(here, "..", "data", "courses", "custom_5km_loop.csv"))
    phys = DEFAULT_PHYSICS
    rider = RIDER_PROFILES["male_tt"]
    mass = rider["rider_mass"] + phys["bike_mass"]
    cp, w_prime = rider["cp"], rider["w_prime"]

    print("Wind sensitivity (one planned ride held into different winds):")
    print(f"{'wind':>12}{'time (s)':>10}{'vs still':>10}")
    wind = wind_sensitivity(course, mass, phys, cp, w_prime, [-4, -2, 0, 2, 4])
    still = next(t for off, t, _ in wind if off == 0)
    for off, total, feasible in wind:
        label = f"+{off:.0f} head" if off > 0 else (f"{off:.0f} tail" if off < 0 else "still")
        note = "" if feasible else "  (reserve blown)"
        print(f"{label:>12}{total:>10.1f}{total - still:>+10.1f}{note}")

    print("\nPower-deviation sensitivity (rider holds 1+dev of the plan):")
    print(f"{'deviation':>12}{'time (s)':>10}{'vs plan':>10}")
    dev_rows = power_deviation_sensitivity(course, mass, phys, cp, w_prime,
                                           [-0.10, -0.05, 0.0, 0.05, 0.10])
    plan_time = next(t for d, t, _ in dev_rows if d == 0.0)
    for dev, total, feasible in dev_rows:
        note = "" if feasible else "  (reserve blown)"
        print(f"{dev * 100:>+11.0f}%{total:>10.1f}{total - plan_time:>+10.1f}{note}")
