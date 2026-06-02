"""Power-curve pacing: spend a finite anaerobic reserve over a course.

Each rider is a critical-power model. They can hold their critical power CP
(watts) for a long time, and they carry W' joules of reserve for riding above
CP. Riding at power P for time t changes the reserve by -(P - CP) * t: it
drains above CP and refills below, and it may never go negative - that is the
rider's energy limit.

Constant-CP pacing never touches the reserve, so it finishes with W' unspent.
Spending that reserve where the rider is slowest - the climbs or the headwind
sections - saves the most time, which is why a paced ride beats a flat one.
"""

from physics import speed_from_power
from parameters import WIND_EXPOSURE


def simulate_pacing(course, powers, mass, phys, cp, w_prime, wind_offset=0.0):
    """Run a course at the given per-segment powers, tracking the W' reserve.

    wind_offset (m/s) is added to every segment's headwind - positive is extra
    headwind, negative is a tailwind. Used by the wind sensitivity analysis.

    Returns (rows, total_time, feasible):
      rows     - list of (segment, power, speed, seg_time, reserve_left)
      feasible - False if the reserve ever ran negative (rider couldn't hold it)
    """
    reserve = w_prime
    feasible = True
    rows = []
    total_time = 0.0
    for seg, power in zip(course, powers):
        wind = WIND_EXPOSURE[seg.wind_exposure] + wind_offset
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


def spend_on_slow_segments(course, mass, phys, cp, w_prime, max_boost=300, step=5):
    """Spend the W' reserve on the slowest segments - the climbs AND the
    headwind sections - because that is where extra power buys the most time.

    Rides CP everywhere, then adds a fixed boost to every segment whose baseline
    (at-CP) speed is below the course average, with the boost set as high as the
    reserve allows without running it negative. This generalises the climbs-only
    idea so it also works on flat, wind-exposed courses where there are no climbs
    to spend the reserve on. Not provably optimal, but it captures the principle
    (ride harder where you are slower) with a concrete, explainable plan.
    """
    base = simulate_pacing(course, constant_cp(course, cp), mass, phys, cp, w_prime)[0]
    speeds = [speed for _seg, _power, speed, _time, _reserve in base]
    avg = sum(speeds) / len(speeds)
    slow = [s < avg for s in speeds]            # below-average speed = the hard segments
    if not any(slow):                           # perfectly uniform course: spend everywhere
        slow = [True] * len(course)

    best = constant_cp(course, cp)
    for boost in range(step, max_boost + 1, step):
        powers = [cp + boost if is_slow else cp for is_slow in slow]
        _, _, feasible = simulate_pacing(course, powers, mass, phys, cp, w_prime)
        if not feasible:
            break
        best = powers
    return best
