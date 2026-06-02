"""Load a course from a CSV of segments."""

import csv
from dataclasses import dataclass


@dataclass
class Segment:
    segment_id: int
    name: str
    distance_m: float
    grade: float            # slope as a fraction (0.04 = 4% up, negative = down)
    turn_penalty_s: float
    wind_exposure: str
    start_m: float = 0.0
    end_m: float = 0.0


def load_course(path):
    """Read a course CSV into a list of Segments, in order."""
    segments = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            segments.append(Segment(
                segment_id=int(row["segment_id"]),
                name=row["name"],
                distance_m=float(row["distance_m"]),
                grade=float(row["grade_pct"]) / 100.0,
                turn_penalty_s=float(row["turn_penalty_s"]),
                wind_exposure=row["wind_exposure"].strip().lower(),
            ))

    # cumulative distance so each segment knows where it starts and ends
    position = 0.0
    for seg in segments:
        seg.start_m = position
        position += seg.distance_m
        seg.end_m = position
    return segments
