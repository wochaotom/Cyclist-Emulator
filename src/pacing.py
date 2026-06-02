"""Power-curve pacing: spend a finite anaerobic reserve over a course.

Each rider is a critical-power model. They can hold their critical power CP
(watts) for a long time, and they carry W' joules of reserve for riding above
CP. Riding at power P for time t changes the reserve by -(P - CP) * t: it
drains above CP and refills below, and it may never go negative - that is the
rider's energy limit.

Constant-CP pacing never touches the reserve, so it finishes with W' unspent.
Spending that reserve where the rider is slowest - the climbs - saves the most
time, which is why a paced ride beats a flat-power ride.
"""

from physics import speed_from_power
from parameters import WIND_EXPOSURE


def simulate_pacing(course, powers, mass, phys, cp, w_prime):
    """Run a course at the given per-segment powers, tracking the W' reserve.

    Returns (rows, total_time, feasible):
      rows     - list of (segment, power, speed, seg_time, reserve_left)
      feasible - False if the reserve ever ran negative (rider couldn't hold it)
    """
    reserve = w_prime
    feasible = True
    rows = []
    total_time = 0.0
    for seg, power in zip(course, powers):
        wind = WIND_EXPOSURE[seg.wind_exposure]
        speed = speed_from_power(power, seg.grade, wind, mass, phys)
        seg_time = seg.distance_m / speed + seg.turn_penalty_s

        reserve -= (power - cp) * seg_time      # drain above CP, refill below
        if reserve < 0:
            feasible = False
        reserve = min(reserve, w_prime)         # cannot bank more than the full reserve

        total_time += seg_time
        rows.append((seg, power, speed, seg_time, reserve))
    return rows, total_time, feasible


def constant_cp(course, cp):
    """Ride at critical power everywhere - never touches the reserve."""
    return [cp] * len(course)


def spend_on_climbs(course, mass, phys, cp, w_prime, max_boost=300, step=5):
    """Ride CP everywhere plus a fixed boost on the climbs, with the boost set
    as high as the W' reserve allows without running it negative.

    Not the provably-optimal plan, but it captures the key idea - spend the
    reserve where the rider is slowest - and gives a concrete strategy to
    compare against constant CP.
    """
    is_climb = [seg.grade > 0 for seg in course]
    best = constant_cp(course, cp)
    for boost in range(step, max_boost + 1, step):
        powers = [cp + boost if climb else cp for climb in is_climb]
        _, _, feasible = simulate_pacing(course, powers, mass, phys, cp, w_prime)
        if not feasible:
            break
        best = powers
    return best
