"""Verify the results/ outputs are correct, complete, and sufficient.

Independent audit harness. It re-loads the model from notebooks/model_v5.ipynb
(without writing any result files), re-optimises each rider/course, and checks the
committed results against it. It also checks data completeness and whether every
required analysis is present.

Prints one PASS/FAIL line per check, then the number of FAILING checks as the
final line - that count is the metric (lower is better, 0 = everything passes).

Run from anywhere: python results/verify_results.py
"""
import json, os, csv

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(REPO, "results")
COURSES_DIR = os.path.join(REPO, "data", "courses")

RIDERS = ["male_tt", "female_tt", "male_climber", "female_climber"]
COURSES = [("tokyo_olympic_tt.csv", "Tokyo"),
           ("flanders_world_tt.csv", "Flanders"),
           ("custom_5km_loop.csv", "Custom")]

checks = []  # (name, passed, detail)
def check(name, passed, detail=""):
    checks.append((name, bool(passed), detail))

def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

# ---- load the model cells once (same approach as sweep.py; we never write files) ----
nb = json.load(open(os.path.join(REPO, "notebooks", "model_v5.ipynb"), encoding="utf-8-sig"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
from scipy.optimize import minimize

def build_sim(rider, course_file):
    """Exec the model's setup cells for one rider/course at one lap; return its namespace."""
    ns = {}
    for i in range(5):  # imports, constants, rider, course, simulate
        s = cells[i]
        if i == 2:
            s = s.replace('rider = "male_tt"', 'rider = "' + rider + '"')
        if i == 3:
            s = s.replace('course_file = "tokyo_olympic_tt.csv"', 'course_file = "' + course_file + '"')
            s = s.replace("laps = 2", "laps = 1")
        exec(compile(s, "cell" + str(i), "exec"), ns)
    return ns

# ---- load the committed results ----
sweep = {r["rider"]: r for r in read_csv(os.path.join(RESULTS, "sweep_results.csv"))}
profiles = {r["profile_id"]: r for r in read_csv(os.path.join(REPO, "data", "rider_profiles.csv"))}
seg_rows = read_csv(os.path.join(RESULTS, "power_by_segment.csv"))
course_km = {label: sum(float(r["distance_m"]) for r in read_csv(os.path.join(COURSES_DIR, cf))) / 1000
             for cf, label in COURSES}
seg_count = {label: len(read_csv(os.path.join(COURSES_DIR, cf))) for cf, label in COURSES}

# ================= Correctness =================
try:
    check("C1 sweep_results has exactly the 4 typed riders",
          set(sweep) == set(RIDERS), "got " + str(sorted(sweep)))
except Exception as e:
    check("C1 sweep_results readable", False, repr(e))

try:  # C2 reproducibility - re-optimise all 12 and compare finishing times
    bad = []
    for cf, label in COURSES:
        for rider in RIDERS:
            ns = build_sim(rider, cf)
            res = minimize(ns["simulate"], x0=[800, 50], method="Nelder-Mead", bounds=[(0, 2000), (0, 150)])
            got = round(res.fun / 60, 1)
            want = float(sweep[rider][label + "_min"])
            if abs(got - want) > 0.2:
                bad.append(rider + "/" + label + " csv=" + str(want) + " rerun=" + str(got))
    check("C2 sweep times reproduce the model (all 12)", not bad, "; ".join(bad))
except Exception as e:
    check("C2 reproducibility", False, repr(e))

try:  # C3 internal consistency - first (flat) segment power == P_base + flat_boost
    bad = []
    for cf, label in COURSES:
        for rider in RIDERS:
            first = next(r for r in seg_rows if r["rider"] == rider and r["course"] == label
                         and int(r["segment"]) == 1)
            expected = float(profiles[rider]["p_base_w"]) + float(sweep[rider][label + "_flat_boost"])
            got = float(first["avg_power_w"])
            if abs(got - expected) > 3:
                bad.append(rider + "/" + label + " expected=" + str(round(expected)) + " got=" + str(round(got)))
    check("C3 flat-segment power == P_base + flat_boost", not bad, "; ".join(bad))
except Exception as e:
    check("C3 internal consistency", False, repr(e))

# ================= Data completeness =================
try:  # D1 power_by_segment covers every rider x course with the right segment count, no empties
    bad = []
    for cf, label in COURSES:
        for rider in RIDERS:
            rows = [r for r in seg_rows if r["rider"] == rider and r["course"] == label]
            if len(rows) != seg_count[label]:
                bad.append(rider + "/" + label + " has " + str(len(rows)) + " segs, want " + str(seg_count[label]))
            if any(not r["avg_power_w"] or float(r["avg_power_w"]) <= 0 for r in rows):
                bad.append(rider + "/" + label + " has empty/non-positive power")
    check("D1 power_by_segment complete (rider x course x segment)", not bad, "; ".join(bad))
except Exception as e:
    check("D1 data completeness", False, repr(e))

try:  # D2 average speeds are physically plausible (25-60 km/h)
    bad = []
    for label in [l for _, l in COURSES]:
        for rider in RIDERS:
            kmh = course_km[label] / (float(sweep[rider][label + "_min"]) / 60)
            if not (25 <= kmh <= 60):
                bad.append(rider + "/" + label + " = " + str(round(kmh, 1)) + " km/h")
    check("D2 average speeds plausible (25-60 km/h)", not bad, "; ".join(bad))
except Exception as e:
    check("D2 speed plausibility", False, repr(e))

try:  # D3 ordering sanity - male_tt fastest, female_climber slowest on each course
    bad = []
    for label in [l for _, l in COURSES]:
        times = {r: float(sweep[r][label + "_min"]) for r in RIDERS}
        if min(times, key=times.get) != "male_tt":
            bad.append(label + " fastest is " + min(times, key=times.get))
        if max(times, key=times.get) != "female_climber":
            bad.append(label + " slowest is " + max(times, key=times.get))
    check("D3 rider ordering sane (male_tt fastest, female_climber slowest)", not bad, "; ".join(bad))
except Exception as e:
    check("D3 ordering", False, repr(e))

try:  # D4 validation - female_tt on the 1-lap Tokyo lands near the real women's winner
    real = read_csv(os.path.join(REPO, "data", "real_results.csv"))
    vv = next(float(r["time_s"]) for r in real
              if r["gender"] == "F" and abs(float(r["distance_km"]) - 22.1) < 0.5)  # van Vleuten, 22.1 km
    model_s = float(sweep["female_tt"]["Tokyo_min"]) * 60
    ratio = model_s / vv
    check("D4 female_tt Tokyo within 0.95-1.35x the real winner", 0.95 <= ratio <= 1.35,
          "ratio=" + str(round(ratio, 3)))
except Exception as e:
    check("D4 validation vs real result", False, repr(e))

# ================= Analysis correctness (the sensitivity outputs must make sense) =================
try:  # C4 wind sensitivity monotonic - more headwind must never make you faster
    path = os.path.join(RESULTS, "wind_sensitivity.csv")
    if os.path.isfile(path):
        rows = read_csv(path)
        bad = []
        for label in set(r["course"] for r in rows):
            pts = sorted((float(r["wind_offset_ms"]), float(r["time_min"]))
                         for r in rows if r["course"] == label)
            times = [t for _, t in pts]
            if any(b < a - 1e-6 for a, b in zip(times, times[1:])):
                bad.append(label)
        check("C4 wind sensitivity monotonic in headwind", not bad, "non-monotonic: " + ",".join(bad))
    else:
        check("C4 wind sensitivity monotonic in headwind", True, "n/a - file absent (S2 covers this)")
except Exception as e:
    check("C4 wind monotonic", False, repr(e))

try:  # C5 power-deviation reproduces the optimum at 0% and is monotonic (more power not slower)
    path = os.path.join(RESULTS, "power_deviation.csv")
    if os.path.isfile(path):
        rows = read_csv(path)
        bad = []
        for rider in set(r["rider"] for r in rows):
            rr = [r for r in rows if r["rider"] == rider]
            zero = next(float(r["time_min"]) for r in rr if int(float(r["deviation_pct"])) == 0)
            if abs(zero - float(sweep[rider]["Tokyo_min"])) > 0.1:
                bad.append(rider + " 0%!=opt")
            pts = sorted((float(r["deviation_pct"]), float(r["time_min"])) for r in rr)
            times = [t for _, t in pts]
            if any(b > a + 1e-6 for a, b in zip(times, times[1:])):
                bad.append(rider + " non-monotonic")
        check("C5 power-deviation reproduces optimum & monotonic", not bad, "; ".join(bad))
    else:
        check("C5 power-deviation reproduces optimum & monotonic", True, "n/a - file absent (S3 covers this)")
except Exception as e:
    check("C5 power-deviation correctness", False, repr(e))

# ================= Sufficiency (required analyses present, with real data) =================
def exists(name):
    return os.path.isfile(os.path.join(RESULTS, name))
def rowcount(name):
    try:
        return len(read_csv(os.path.join(RESULTS, name)))
    except Exception:
        return 0

check("S1 power-distribution analysis present",
      exists("power_by_segment.csv") and exists("power_tokyo.png") and exists("finish_times.png"))
check("S2 wind sensitivity present (csv >= 9 rows + plot)",
      exists("wind_sensitivity.csv") and rowcount("wind_sensitivity.csv") >= 9 and exists("wind_sensitivity.png"))
check("S3 power-deviation sensitivity present (csv >= 7 rows + plot)",
      exists("power_deviation.csv") and rowcount("power_deviation.csv") >= 7 and exists("power_deviation.png"))
check("S4 results documented (results/README.md present)", exists("README.md"))

# ================= Report =================
fails = sum(1 for _, p, _ in checks if not p)
for name, p, d in checks:
    print(("PASS" if p else "FAIL") + "  " + name + (("  -- " + d) if (d and not p) else ""))
print()
print(fails)
