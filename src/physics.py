"""Speed and time from power for a single course segment.

For a steady speed v on a segment with a given grade and headwind, the rider's
power has to cover aerodynamic drag, rolling resistance, and gravity:

    P = v * ( 0.5 * rho * CdA * (v + wind)**2     # aerodynamic drag
              + Crr * m * g                        # rolling resistance
              + m * g * grade )                    # gravity along the slope

We know the rider's power and want the speed, so we solve this for v. There is
no tidy closed form (it is cubic in v), so we bisect on a speed range.
"""


def power_required(v, grade, wind, mass, phys):
    """Power (W) needed to hold steady speed v (m/s) on a segment."""
    drag = 0.5 * phys["rho"] * phys["CdA"] * (v + wind) ** 2
    rolling = phys["Crr"] * mass * phys["g"]
    gravity = mass * phys["g"] * grade
    return v * (drag + rolling + gravity)


def speed_from_power(power, grade, wind, mass, phys, tol=1e-4):
    """Steady speed (m/s) a rider holds on a segment given their power (W)."""
    # power_required(0) = 0 and it grows with speed, so for any positive power
    # there is a single speed that matches it. Find an upper bound that is too
    # fast, then bisect down to the answer.
    low, high = 0.0, 30.0
    while power_required(high, grade, wind, mass, phys) < power:
        high *= 1.5
        if high > 300.0:        # unrealistic - stop instead of looping forever
            break

    while high - low > tol:
        mid = 0.5 * (low + high)
        if power_required(mid, grade, wind, mass, phys) < power:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)
