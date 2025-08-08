"""Pydantic models for FIT parsing."""

from pydantic import BaseModel
from typing import List, Optional

class Record(BaseModel):
    timestamp: Optional[int] = None
    power: Optional[float] = None
    developer_fields: Optional[dict] = None
    speed_m_s: Optional[float] = None
    pace_s_km: Optional[float] = None
    grade_pct: Optional[float] = None

class Lap(BaseModel):
    start: Optional[int] = None
    end: Optional[int] = None

class Event(BaseModel):
    type: Optional[str] = None
    timestamp: Optional[int] = None

class Workout(BaseModel):
    header: dict
    records: List[Record] = []
    laps: List[Lap] = []
    events: List[Event] = []
