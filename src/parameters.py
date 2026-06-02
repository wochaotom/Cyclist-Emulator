# Physics constants and rider profiles.
# Starting values for the group to refine during course parameterization.

DEFAULT_PHYSICS = {
    "rho": 1.225,      # air density (kg/m^3)
    "CdA": 0.25,       # drag area = drag coefficient * frontal area (m^2)
    "Crr": 0.005,      # rolling resistance coefficient
    "g": 9.81,         # gravity (m/s^2)
    "bike_mass": 8.0,  # bike mass (kg)
}

# The two rider types the problem asks for: a time-trial specialist and a
# climber, each as a male and female profile. Each rider is a critical-power
# model: they hold CP (watts) for a long time and carry a finite reserve W'
# (joules) for going above CP, which refills when they ride below it.
#   cp       - critical power, watts
#   w_prime  - anaerobic work capacity, joules
# Placeholder values - refine from rider data during parameterization.
RIDER_PROFILES = {
    "male_tt":        {"rider_mass": 75, "cp": 350, "w_prime": 22000},
    "female_tt":      {"rider_mass": 62, "cp": 270, "w_prime": 16000},
    "male_climber":   {"rider_mass": 65, "cp": 330, "w_prime": 18000},
    "female_climber": {"rider_mass": 55, "cp": 250, "w_prime": 14000},
}

# Effective headwind (m/s) we assume for each wind-exposure label used in the
# course files. Placeholder mapping - tune during course parameterization.
WIND_EXPOSURE = {
    "low": 0.0,
    "medium": 1.0,
    "high": 2.0,
}
