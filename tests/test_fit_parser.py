import os
from ai_sport_agent.parsers.base_parser import StubParser

def test_stub_parser_minimal_fit(tmp_path):
    fit_path = tmp_path / "minimal.fit"
    fit_path.write_bytes(bytes([12]) + bytes(11))
    parser = StubParser()
    result = parser.parse(fit_path)
    assert "protocol" in result.header and result.header["protocol"] == 0
    assert "profile" in result.header and result.header["profile"] == 0
    assert result.records == []
