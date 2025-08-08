import struct

def make_fit_with_devfields(path):
    # Minimal FIT with developer field definition and one data message
    with open(path, "wb") as f:
        # Header: size=14, protocol=0, profile=0, data_size=10
        f.write(bytes([14, 0, 0]) + struct.pack("<I", 10) + b".FIT" + b"\x00" * 2)
        # Definition message (local_type=0, developer data flag set)
        f.write(bytes([0xA0]))  # def header: 0x80 (definition) | 0x20 (developer data)
        f.write(bytes([0, 0]))  # reserved, arch
        f.write(struct.pack("<H", 20))  # global_msg_num
        f.write(bytes([2]))  # num_fields
        # field_num=253 (timestamp, 4 bytes), field_num=1 (1 byte)
        f.write(bytes([253, 4, 0]))  # timestamp field
        f.write(bytes([1, 1, 0]))    # field_num=1, size=1, base_type=0
        f.write(bytes([1]))  # num_dev_fields
        f.write(bytes([2, 1, 0]))  # dev_field_num, size, dev_idx
        # Data message (local_type=0)
        f.write(bytes([0x00]))  # data header
        f.write(struct.pack("<I", 123456))  # timestamp value
        f.write(bytes([5]))     # field value
        f.write(bytes([7]))     # dev field value

def make_compressed_ts_fit(path):
    with open(path, "wb") as f:
        f.write(bytes([14, 0, 0]) + struct.pack("<I", 15) + b".FIT" + b"\x00" * 2)
        # Definition message (local_type=0)
        f.write(bytes([0x80]))
        f.write(bytes([0, 0]))
        f.write(struct.pack("<H", 20))
        f.write(bytes([1]))
        f.write(bytes([253, 4, 0]))
        f.write(bytes([0]))
        # Data messages with compressed timestamp headers (local_type=0)
        for ts in [32, 64, 96]:
            header = 0x60 | (ts % 32)
            f.write(bytes([header]))
            f.write(struct.pack("<I", ts))

def test_fit_devfields_parser(fit_file):
    """Test parsing of FIT file with developer fields."""
    from ai_sport_agent.parsers.fit_parser import FitParser

    parser = FitParser(fit_file)
    records = parser.parse()

    # Check that developer fields are present and correctly parsed
    for record in records:
        assert hasattr(record, 'developer_fields')
        assert isinstance(record.developer_fields, dict)
        assert 'dev_field_1' in record.developer_fields
        assert record.developer_fields['dev_field_1'] == 7

def test_compressed_ts_parser(fit_file):
    """Test parsing of compressed timestamp headers in FIT file."""
    from ai_sport_agent.parsers.fit_parser import FitParser

    parser = FitParser(fit_file)
    records = parser.parse()

    # Check that timestamps are correctly reconstructed
    assert records[0].timestamp == 32
    assert records[1].timestamp == 64
    assert records[2].timestamp == 96

def test_derived_fields(records):
    """Test derived fields calculation: speed, pace, grade."""
    from ai_sport_agent.parsers.fit_parser import FitParser

    # Assuming records are already parsed FIT records
    for record in records:
        if hasattr(record, 'speed'):
            assert record.speed >= 0
        if hasattr(record, 'pace'):
            assert record.pace > 0
        if hasattr(record, 'grade'):
            assert record.grade is not None and record.grade != float('inf')
