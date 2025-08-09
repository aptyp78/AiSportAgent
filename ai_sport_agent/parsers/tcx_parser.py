import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List
from ai_sport_agent.core.models import Workout, Lap, Record, Event

def parse_tcx(path: Path) -> Workout:
    tree = ET.parse(path)
    root = tree.getroot()
    laps: List[Lap] = []
    records: List[Record] = []
    events: List[Event] = []
    for lap in root.findall(".//Lap"):
        lap_start, lap_end = None, None
        lap_records = []
        for tp in lap.findall(".//Trackpoint"):
            time_str = tp.findtext("Time")
            lat = tp.findtext("Position/LatitudeDegrees")
            lon = tp.findtext("Position/LongitudeDegrees")
            ele = tp.findtext("AltitudeMeters")
            dist = tp.findtext("DistanceMeters")
            hr = tp.findtext("HeartRateBpm/Value")
            timestamp = None
            if time_str:
                import datetime
                timestamp = int(datetime.datetime.fromisoformat(time_str.replace("Z", "+00:00")).timestamp())
            rec = Record(
                timestamp=timestamp,
                power=None,
                developer_fields={"hr": int(hr)} if hr else None,
                speed_m_s=None,
                pace_s_km=None,
                grade_pct=None
            )
            lap_records.append(rec)
            if lap_start is None:
                lap_start = timestamp
            lap_end = timestamp
        laps.append(Lap(start=lap_start, end=lap_end))
        records.extend(lap_records)
    records = compute_derived_fields(records)
    return Workout(header={"source": "tcx"}, records=records, laps=laps, events=events)

def compute_derived_fields(records: List[Record]) -> List[Record]:
    window = 3
    for i, rec in enumerate(records):
        speeds = []
        grades = []
        for j in range(max(0, i - window), min(len(records), i + window + 1)):
            r = records[j]
            speed = r.developer_fields.get("hr") if r.developer_fields else None
            if speed is not None and speed >= 0:
                speeds.append(speed)
            grade = 0
            grades.append(grade)
        rec.speed_m_s = sum(speeds) / len(speeds) if speeds else None
        rec.pace_s_km = 1000 / rec.speed_m_s if rec.speed_m_s and rec.speed_m_s > 0 else None
        rec.grade_pct = sum(grades) / len(grades) if grades else None
    return records
