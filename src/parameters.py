# Physics constants and rider profiles.
# Starting values for the group to refine during course parameterization.

DEFAULT_PHYSICS = {
    "rho": 1.225,      # air density (kg/m^3)
    "CdA": 0.21,       # drag area, m^2 (elite TT/aero position ~0.20-0.22)
    "Crr": 0.004,      # rolling resistance (fast road TT tire on good asphalt)
    "g": 9.81,         # gravity (m/s^2)
    "bike_mass": 8.0,  # bike mass (kg)
}

# The two rider types the problem requires - a time-trial specialist (high
# absolute power, more aero, a bit heavier) and a climber (higher power-to-
# weight, lighter, lower absolute power) - each as a male and female profile,
# so 2 types x 2 genders.
#   rider_mass - rider's BODY mass in kg, NOT including the bike. The model
#                uses total mass = rider_mass + bike_mass.
#   cp         - critical power, watts (held for a long time)
#   w_prime    - anaerobic reserve, joules (energy available above CP)
# Values sit inside sourced ranges (see references/data-sources.md); the
# climber carries the higher W/kg, the TT specialist the higher absolute watts.
RIDER_PROFILES = {
    "male_tt":        {"rider_mass": 75, "cp": 350, "w_prime": 22000},  # 4.7 W/kg
    "female_tt":      {"rider_mass": 62, "cp": 270, "w_prime": 16000},  # 4.4 W/kg
    "male_climber":   {"rider_mass": 65, "cp": 330, "w_prime": 18000},  # 5.1 W/kg
    "female_climber": {"rider_mass": 55, "cp": 250, "w_prime": 14000},  # 4.5 W/kg
}

# Effective headwind (m/s) we assume for each wind-exposure label used in the
# course files. Placeholder mapping - tune during course parameterization.
WIND_EXPOSURE = {
    "low": 0.0,
    "medium": 1.0,
    "high": 2.0,
}
