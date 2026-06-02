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
# climber, each as a male and female profile. `sustainable_power` is a single
# constant-power stand-in for now - it becomes a full power curve (max power vs
# duration) plus an energy budget once we move past the baseline model.
RIDER_PROFILES = {
    "male_tt":        {"rider_mass": 75, "sustainable_power": 320},
    "female_tt":      {"rider_mass": 62, "sustainable_power": 240},
    "male_climber":   {"rider_mass": 65, "sustainable_power": 290},
    "female_climber": {"rider_mass": 55, "sustainable_power": 220},
}

# Effective headwind (m/s) we assume for each wind-exposure label used in the
# course files. Placeholder mapping - tune during course parameterization.
WIND_EXPOSURE = {
    "low": 0.0,
    "medium": 1.0,
    "high": 2.0,
}
