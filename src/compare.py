"""Compare every rider on every course - the rider x course matchup.

For each (rider, course) it reports the paced finishing time. Then, for each
gender, it shows the climber's time minus the TT specialist's: a negative gap
means the climber is faster (expected where there is climbing), positive means
the TT specialist wins (expected on the flat). The gap flipping sign across
courses is the cross-over the problem is built around.

Tokyo is run as one 22.1 km lap for all riders so the comparison isolates rider
type (the men's event is two laps).
"""

import os

from course import load_course
from pacing import simulate_pacing, spend_on_slow_segments
from parameters import DEFAULT_PHYSICS, RIDER_PROFILES


def paced_time(course, rider, phys=DEFAULT_PHYSICS):
    """Total finishing time for a rider's paced ride on a course."""
    mass = rider["rider_mass"] + phys["bike_mass"]
    plan = spend_on_slow_segments(course, mass, phys, rider["cp"], rider["w_prime"])
    _, total, _ = simulate_pacing(course, plan, mass, phys, rider["cp"], rider["w_prime"])
    return total


def matchup(courses, riders=RIDER_PROFILES):
    """Return {rider_name: {course_name: time_s}}."""
    return {name: {cn: paced_time(c, r) for cn, c in courses.items()}
            for name, r in riders.items()}


if __name__ == "__main__":
    cdir = os.path.join(os.path.dirname(__file__), "..", "data", "courses")
    courses = {
        "custom": load_course(os.path.join(cdir, "custom_5km_loop.csv")),
        "Tokyo": load_course(os.path.join(cdir, "tokyo_olympic_tt.csv")),
        "Flanders": load_course(os.path.join(cdir, "flanders_world_tt.csv")),
    }
    table = matchup(courses)
    names = list(courses.keys())

    print("Finishing time (s) by rider and course:")
    print(f"{'rider':16}" + "".join(f"{n:>12}" for n in names))
    for rname in RIDER_PROFILES:
        print(f"{rname:16}" + "".join(f"{table[rname][n]:>12.1f}" for n in names))

    print("\nClimber - TT specialist  (negative = climber faster):")
    for sex in ("male", "female"):
        line = f"  {sex:8}"
        for n in names:
            gap = table[f"{sex}_climber"][n] - table[f"{sex}_tt"][n]
            line += f"{gap:>+12.1f}"
        print(line)
