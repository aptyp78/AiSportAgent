import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional
from math import radians, cos, sin, sqrt, atan2
from ai_sport_agent.core.models import Workout, Lap, Record, Event

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

def parse_gpx(path: Path) -> Workout:
    tree = ET.parse(path)
    root = tree.getroot()
    ns = {"gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1"}
    laps: List[Lap] = []
    records: List[Record] = []
    events: List[Event] = []
    for trk in root.findall(".//trk"):
        for seg in trk.findall("trkseg"):
            lap_start, lap_end = None, None
            prev_lat, prev_lon, prev_time = None, None, None
            lap_records = []
            for pt in seg.findall("trkpt"):
                lat = float(pt.attrib["lat"])
                lon = float(pt.attrib["lon"])
                ele = float(pt.findtext("ele", "0"))
                time_str = pt.findtext("time")
                hr = pt.findtext("gpxtpx:hr", None, ns)
                timestamp = None
                if time_str:
                    import datetime
                    timestamp = int(datetime.datetime.fromisoformat(time_str.replace("Z", "+00:00")).timestamp())
                dist = None
                if prev_lat is not None and prev_lon is not None:
                    dist = haversine(prev_lat, prev_lon, lat, lon)
                rec = Record(
                    timestamp=timestamp,
                    power=None,
                    developer_fields={"hr": int(hr)} if hr else None,
                    speed_m_s=None,
                    pace_s_km=None,
                    grade_pct=None
                )
                lap_records.append(rec)
                prev_lat, prev_lon, prev_time = lat, lon, timestamp
                if lap_start is None:
                    lap_start = timestamp
                lap_end = timestamp
            laps.append(Lap(start=lap_start, end=lap_end))
            records.extend(lap_records)
    records = compute_derived_fields(records)
    return Workout(header={"source": "gpx"}, records=records, laps=laps, events=events)

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
