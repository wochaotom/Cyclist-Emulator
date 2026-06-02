"""Run one rider over one course at constant power and report segment times."""

import os

from course import load_course
from physics import speed_from_power
from parameters import DEFAULT_PHYSICS, RIDER_PROFILES, WIND_EXPOSURE


def simulate(course_path, rider_name, phys=DEFAULT_PHYSICS):
    """Return per-segment (segment, speed, time) rows and the total race time."""
    course = load_course(course_path)
    rider = RIDER_PROFILES[rider_name]
    mass = rider["rider_mass"] + phys["bike_mass"]
    power = rider["sustainable_power"]

    rows = []
    total_time = 0.0
    for seg in course:
        wind = WIND_EXPOSURE[seg.wind_exposure]
        speed = speed_from_power(power, seg.grade, wind, mass, phys)
        seg_time = seg.distance_m / speed + seg.turn_penalty_s
        total_time += seg_time
        rows.append((seg, speed, seg_time))
    return rows, total_time


def print_report(rows, total_time, rider_name):
    print(f"Rider: {rider_name}")
    print(f"{'id':>2}  {'segment':<18}{'dist(m)':>8}{'grade':>7}"
          f"{'speed(m/s)':>11}{'km/h':>7}{'time(s)':>9}")
    for seg, speed, seg_time in rows:
        print(f"{seg.segment_id:>2}  {seg.name:<18}{seg.distance_m:>8.0f}"
              f"{seg.grade * 100:>6.1f}%{speed:>11.2f}{speed * 3.6:>7.1f}{seg_time:>9.1f}")
    print(f"\nTotal time: {total_time:.1f} s  ({total_time / 60:.2f} min)")


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    course_path = os.path.join(here, "..", "data", "courses", "custom_5km_loop.csv")
    rows, total_time = simulate(course_path, "male_tt")
    print_report(rows, total_time, "male_tt")
