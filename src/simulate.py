"""Run one rider over one course and compare constant-power vs paced riding."""

import os

from course import load_course
from pacing import simulate_pacing, constant_cp, spend_on_slow_segments
from parameters import DEFAULT_PHYSICS, RIDER_PROFILES


def run(course_path, rider_name, phys=DEFAULT_PHYSICS):
    course = load_course(course_path)
    rider = RIDER_PROFILES[rider_name]
    mass = rider["rider_mass"] + phys["bike_mass"]
    cp, w_prime = rider["cp"], rider["w_prime"]

    flat_powers = constant_cp(course, cp)
    paced_powers = spend_on_slow_segments(course, mass, phys, cp, w_prime)

    flat = simulate_pacing(course, flat_powers, mass, phys, cp, w_prime)
    paced = simulate_pacing(course, paced_powers, mass, phys, cp, w_prime)
    return cp, w_prime, flat, paced


def print_report(rider_name, cp, w_prime, flat, paced):
    flat_rows, flat_time, _ = flat
    paced_rows, paced_time, _ = paced

    print(f"Rider: {rider_name}    CP = {cp} W    W' = {w_prime / 1000:.0f} kJ\n")
    print("Paced ride (spend the reserve on the slow sections):")
    print(f"{'id':>2}  {'segment':<18}{'power':>7}{'speed':>8}{'km/h':>7}"
          f"{'time':>8}{'reserve(kJ)':>13}")
    for seg, power, speed, seg_time, reserve in paced_rows:
        print(f"{seg.segment_id:>2}  {seg.name:<18}{power:>7.0f}{speed:>8.2f}"
              f"{speed * 3.6:>7.1f}{seg_time:>8.1f}{reserve / 1000:>13.2f}")

    print(f"\nConstant CP : {flat_time:8.1f} s  ({flat_time / 60:.2f} min)")
    print(f"Paced       : {paced_time:8.1f} s  ({paced_time / 60:.2f} min)")
    print(f"Time saved  : {flat_time - paced_time:8.1f} s  by spending the W' reserve")


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    course_path = os.path.join(here, "..", "data", "courses", "custom_5km_loop.csv")
    cp, w_prime, flat, paced = run(course_path, "male_tt")
    print_report("male_tt", cp, w_prime, flat, paced)
