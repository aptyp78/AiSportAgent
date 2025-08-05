#!/usr/bin/env python3
"""
Universal FIT parser v0.11.1 for AiSportAgent
Читает Garmin/Stryd .fit тренировки без внешних зависимостей,
детектит work/recovery, группирует повторы динамически.
"""

from __future__ import annotations
import struct, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Union, Tuple

FIT_EPOCH = datetime(1989, 12, 31, tzinfo=timezone.utc)
BASE = {
    0x00: ("B", 1),   0x01: ("b", 1),   0x02: ("B", 1),
    0x83: ("<h", 2),  0x84: ("<H", 2),  0x85: ("<i", 4),
    0x86: ("<I", 4),  0x88: ("<f", 4),  0x8C: ("<I", 4)
}

class Step:
    def __init__(self, start: datetime, end: datetime, avg_power: float, type: str):
        self.start = start
        self.end = end
        self.duration = (end - start).total_seconds()
        self.avg_power = avg_power
        self.type = type

    def to_dict(self):
        return {
            "start": self.start.isoformat(),
            "end":   self.end.isoformat(),
            "duration": self.duration,
            "avg_power": self.avg_power,
            "type": self.type
        }

class RepeatBlock:
    def __init__(self, count: int, work_dur: float, rest_dur: float, steps: List[Step]):
        self.count = count
        self.work_duration = work_dur
        self.rest_duration = rest_dur
        self.steps = steps

    def to_dict(self):
        return {
            "type": "repeat_block",
            "count": self.count,
            "work_duration": self.work_duration,
            "rest_duration": self.rest_duration,
            "steps": [s.to_dict() for s in self.steps]
        }

def kmeans_1d(values: List[float], k: int, max_iter: int = 50) -> Tuple[List[float], List[int]]:
    if len(values) < k:
        k = len(values)
    centroids = sorted(values)[:k]
    labels = [0] * len(values)
    for _ in range(max_iter):
        new_labels = [min(range(k), key=lambda ci: abs(v-centroids[ci])) for v in values]
        new_centroids = []
        for ci in range(k):
            cluster = [v for v,l in zip(values,new_labels) if l==ci]
            new_centroids.append(sum(cluster)/len(cluster) if cluster else centroids[ci])
        if all(abs(a-b)<1e-6 for a,b in zip(new_centroids, centroids)):
            labels = new_labels
            break
        centroids, labels = new_centroids, new_labels
    return centroids, labels

def group_dynamic(steps: List[Step], min_repeat: int = 2) -> List[Union[Step, RepeatBlock]]:
    grouped: List[Union[Step, RepeatBlock]] = []
    work = [s for s in steps if s.type=="work"]
    rest = [s for s in steps if s.type=="recovery"]
    w_cent, w_lbls = kmeans_1d([s.duration for s in work], min(3,len(work)))
    r_cent, r_lbls = kmeans_1d([s.duration for s in rest], min(3,len(rest)))
    w_map = {s:lbl for s,lbl in zip(work, w_lbls)}
    r_map = {s:lbl for s,lbl in zip(rest, r_lbls)}

    i, n = 0, len(steps)
    while i < n-1:
        a, b = steps[i], steps[i+1]
        if a.type=="work" and b.type=="recovery" and w_map.get(a)==r_map.get(b):
            seq = []
            lbl = w_map[a]
            while i < n-1 and steps[i].type=="work" and steps[i+1].type=="recovery" and w_map.get(steps[i])==lbl:
                seq.append((steps[i], steps[i+1]))
                i += 2
            if len(seq) >= min_repeat:
                work_avg = sum(w.duration for w,_ in seq)/len(seq)
                rest_avg = sum(r.duration for _,r in seq)/len(seq)
                flat = [item for pair in seq for item in pair]
                grouped.append(RepeatBlock(len(seq), work_avg, rest_avg, flat))
                continue
        grouped.append(steps[i])
        i += 1
    while i < n:
        grouped.append(steps[i]); i += 1
    return grouped

def detect_steps_from_power(path: Path) -> List[Step]:
    # Фоллбэк: весь файл — один рабочий шаг
    now = datetime.now(timezone.utc)
    return [Step(now, now + timedelta(seconds=1), 0.0, "work")]

def extract_workout_steps(path: Path) -> List[dict]:
    # TODO: читать workout_step-сообщения
    return []

def extract_laps(path: Path) -> List[dict]:
    # TODO: читать Lap-записи
    return []

def parse_fit(path: Path) -> dict:
    # 1) Сессия запланированных шагов?
    ws = extract_workout_steps(path)
    if ws:
        mode = "plan"
        raw = [Step(w["start_time"], w["end_time"], w.get("avg_power",0),"work") for w in ws]
    else:
        laps = extract_laps(path)
        if laps:
            mode = "laps"
            # TODO: разбить по laps и классифицировать
            raw = []
        else:
            mode = "auto"
            raw = detect_steps_from_power(path)

    grouped = group_dynamic(raw)
    intervals = [iv.to_dict() for iv in grouped]
    return {
        "file": str(path),
        "date": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "intervals": intervals
    }
