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
        protocol_version = f.read(1)[0]
        profile_version = struct.unpack("<H", f.read(2))[0]
        data_size = struct.unpack("<I", f.read(4))[0]
        data_type = f.read(4)
        crc = f.read(header_size - 12) if header_size > 12 else b''
        print(f"header_size={header_size}, protocol_version={protocol_version}, profile_version={profile_version}, data_size={data_size}, data_type={data_type}, crc={crc}")
        data_start = f.tell()
        definitions = {}
        dev_field_defs = {}
        records: List[Record] = []
        last_timestamp = None
        base_timestamp = None

        while f.tell() - data_start < data_size:
            print(f"Loop: f.tell()={f.tell()}, data_start={data_start}, data_size={data_size}")
            rec_header_b = f.read(1)
            print(f"Read rec_header_b: {rec_header_b}")
            if not rec_header_b:
                print("No rec_header_b, breaking loop.")
                break
            rec_header = rec_header_b[0]
            is_def = (rec_header & 0x80) != 0
            local_type = rec_header & 0x0F
            dev_data_flag = (rec_header & 0x20) != 0
            is_compressed_ts = (rec_header & 0x60) == 0x60
            print(f"Parsed header: rec_header={rec_header}, is_def={is_def}, local_type={local_type}, dev_data_flag={dev_data_flag}, is_compressed_ts={is_compressed_ts}")
            if is_def:
                print(f"Definition message: header_byte={rec_header_b.hex()}, local_type={local_type}, dev_data_flag={dev_data_flag}")
                print(f"definitions before: {definitions}")
                reserved_bytes = f.read(2)
                print(f"reserved_bytes: {reserved_bytes.hex()}")
                reserved, arch = struct.unpack("BB", reserved_bytes)
                print(f"reserved={reserved}, arch={arch}")
                global_msg_num_bytes = f.read(2)
                print(f"global_msg_num_bytes: {global_msg_num_bytes.hex()}")
                endian = "<" if arch == 0 else ">"
                global_msg_num = struct.unpack(endian + "H", global_msg_num_bytes)[0]
                print(f"global_msg_num={global_msg_num}")
                num_fields_byte = f.read(1)
                print(f"num_fields_byte: {num_fields_byte.hex()}")
                num_fields = num_fields_byte[0]
                fields = []
                total = 0
                for i in range(num_fields):
                    field_bytes = f.read(3)
                    print(f"field_bytes[{i}]: {field_bytes.hex()}")
                    field_num, size, base_type = struct.unpack("BBB", field_bytes)
                    fields.append((field_num, size, base_type))
                    total += size
                dev_fields = []
                if dev_data_flag:
                    num_dev_fields_byte = f.read(1)
                    print(f"num_dev_fields_byte: {num_dev_fields_byte.hex()}")
                    num_dev_fields = num_dev_fields_byte[0]
                    for i in range(num_dev_fields):
                        dev_field_bytes = f.read(3)
                        print(f"dev_field_bytes[{i}]: {dev_field_bytes.hex()}")
                        field_num, size, dev_idx = struct.unpack("BBB", dev_field_bytes)
                        dev_fields.append((field_num, size, dev_idx))
                        total += size
                definitions[local_type] = {
                    "endian": endian,
                    "fields": fields,
                    "dev_fields": dev_fields,
                    "size": total,
                    "global_msg_num": global_msg_num,
                }
                print(f"definitions after: {definitions}")
                print(f"Definition for local_type {local_type} added: {definitions.get(local_type)}")
            else:
                print(f"Data message: local_type={local_type}, defn={definitions.get(local_type)}")
                print(f"definitions at data message: {definitions}")
                defn = definitions.get(local_type)
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
