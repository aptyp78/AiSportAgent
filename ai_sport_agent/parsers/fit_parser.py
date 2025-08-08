"""FIT parser: developer fields, compressed timestamps, derived fields."""

import struct
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta, timezone
from ai_sport_agent.core.models import Record, Workout

FIT_EPOCH = datetime(1989, 12, 31, tzinfo=timezone.utc)

def parse_fit(path: Path) -> Workout:
    with path.open("rb") as f:
        header_size = f.read(1)[0]
        header = f.read(header_size - 1)
        protocol_version = header[0]
        profile_version = struct.unpack("<H", header[1:3])[0]
        data_size = struct.unpack("<I", header[3:7])[0]
        data_start = f.tell()
        definitions = {}
        dev_field_defs = {}
        records: List[Record] = []
        last_timestamp = None
        base_timestamp = None

        while f.tell() - data_start < data_size:
            rec_header_b = f.read(1)
            if not rec_header_b:
                break
            rec_header = rec_header_b[0]
            is_def = (rec_header & 0x80) != 0
            local_type = rec_header & 0x0F
            dev_data_flag = (rec_header & 0x20) != 0
            is_compressed_ts = (rec_header & 0x60) == 0x60

            if is_def:
                reserved, arch = struct.unpack("BB", f.read(2))
                endian = "<" if arch == 0 else ">"
                global_msg_num = struct.unpack(endian + "H", f.read(2))[0]
                num_fields = f.read(1)[0]
                fields = []
                total = 0
                for _ in range(num_fields):
                    field_num, size, base_type = struct.unpack("BBB", f.read(3))
                    fields.append((field_num, size, base_type))
                    total += size
                dev_fields = []
                if dev_data_flag:
                    num_dev_fields = f.read(1)[0]
                    for _ in range(num_dev_fields):
                        field_num, size, dev_idx = struct.unpack("BBB", f.read(3))
                        dev_fields.append((field_num, size, dev_idx))
                        total += size
                    dev_field_defs[local_type] = dev_fields
                definitions[local_type] = {
                    "endian": endian,
                    "fields": fields,
                    "dev_fields": dev_fields,
                    "size": total,
                    "global_msg_num": global_msg_num,
                }
            else:
                defn = definitions.get(local_type)
                print(f"Data message: local_type={local_type}, defn={defn}")
                if not defn:
                    print("No definition for local_type, skipping.")
                    break
                raw = f.read(defn["size"])
                print(f"Raw data ({len(raw)} bytes): {raw.hex()}")
                if len(raw) < defn["size"]:
                    print("Incomplete data message, skipping.")
                    continue  # skip incomplete data
                offset = 0
                timestamp = None
                developer_fields: Dict[str, Any] = {}
                # Compressed timestamp header
                if is_compressed_ts:
                    ts_offset = rec_header & 0x1F
                    if last_timestamp is None:
                        last_timestamp = 0
                    timestamp = (last_timestamp & ~0x1F) + ts_offset
                    if timestamp < last_timestamp:
                        timestamp += 32
                    last_timestamp = timestamp
                    timestamp = FIT_EPOCH + timedelta(seconds=timestamp)
                # Standard fields
                for field_num, size, base_type in defn["fields"]:
                    chunk = raw[offset : offset + size]
                    print(f"Field {field_num}: {chunk.hex()}")
                    if field_num == 253 and size == 4:
                        if len(chunk) == 4:
                            val = struct.unpack(defn["endian"] + "I", chunk)[0]
                            print(f"Timestamp value: {val}")
                            timestamp = FIT_EPOCH + timedelta(seconds=val)
                            last_timestamp = val
                    elif field_num == 7 and size == 2:
                        if len(chunk) == 2:
                            power = struct.unpack(defn["endian"] + "H", chunk)[0]
                            print(f"Power value: {power}")
                    offset += size
                # Developer fields
                for field_num, size, dev_idx in defn["dev_fields"]:
                    chunk = raw[offset : offset + size]
                    print(f"DevField {field_num}: {chunk.hex()}")
                    if len(chunk) == size:
                        developer_fields[f"dev_{field_num}"] = int.from_bytes(chunk, "little")
                    offset += size
                rec = Record(
                    timestamp=int(timestamp.timestamp()) if timestamp else None,
                    power=locals().get("power"),
                    developer_fields=developer_fields if developer_fields else None
                )
                print(f"Record: {rec}")
                records.append(rec)

    # Derived fields post-process
    records = compute_derived_fields(records)
    return Workout(
        header={"protocol": protocol_version, "profile": profile_version},
        records=records,
        laps=[],
        events=[]
    )

def compute_derived_fields(records: List[Record]) -> List[Record]:
    # Calculate speed_m_s, pace_s_km, grade_pct with sliding window
    window = 3
    for i, rec in enumerate(records):
        speeds = []
        grades = []
        for j in range(max(0, i - window), min(len(records), i + window + 1)):
            r = records[j]
            # Example: speed_m_s from developer_fields or other logic
            speed = r.developer_fields.get("dev_1") if r.developer_fields else None
            if speed is not None and speed >= 0:
                speeds.append(speed)
            # Example: grade_pct from dev_2
            grade = r.developer_fields.get("dev_2") if r.developer_fields else None
            if grade is not None:
                grades.append(grade)
        rec.speed_m_s = sum(speeds) / len(speeds) if speeds else None
        rec.pace_s_km = 1000 / rec.speed_m_s if rec.speed_m_s and rec.speed_m_s > 0 else None
        rec.grade_pct = sum(grades) / len(grades) if grades else None
    return records
