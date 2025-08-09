import json
import math
from pathlib import Path
from ai_sport_agent.cli import app as cli_app
from typer.testing import CliRunner
from fastapi.testclient import TestClient
from ai_sport_agent.api.v1 import app as api_app

def check_workout_json(json_data):
    assert "laps" in json_data
    assert "records" in json_data
    assert isinstance(json_data["records"], list)
    for rec in json_data["records"]:
        if "speed_m_s" in rec and rec["speed_m_s"] is not None:
            assert rec["speed_m_s"] >= 0
            if rec["speed_m_s"] > 0:
                assert rec["pace_s_km"] > 0
        if "grade_pct" in rec:
            assert not (math.isnan(rec["grade_pct"]) or math.isinf(rec["grade_pct"]))

def test_gpx_cli_export(tmp_path):
    src = Path("tests/data/mini.gpx")
    out = tmp_path / "out.json"
    runner = CliRunner()
    result = runner.invoke(cli_app, ["export", str(src), "--json", str(out)])
    assert result.exit_code == 0
    data = json.loads(out.read_text())
    check_workout_json(data)

def test_tcx_cli_export(tmp_path):
    src = Path("tests/data/mini.tcx")
    out = tmp_path / "out.json"
    runner = CliRunner()
    result = runner.invoke(cli_app, ["export", str(src), "--json", str(out)])
    assert result.exit_code == 0
    data = json.loads(out.read_text())
    check_workout_json(data)

def test_gpx_api_parse():
    client = TestClient(api_app)
    with open("tests/data/mini.gpx", "rb") as f:
        resp = client.post("/v1/parse", files={"file": ("mini.gpx", f, "application/gpx+xml")})
    assert resp.status_code == 200
    check_workout_json(resp.json())

def test_tcx_api_parse():
    client = TestClient(api_app)
    with open("tests/data/mini.tcx", "rb") as f:
        resp = client.post("/v1/parse", files={"file": ("mini.tcx", f, "application/xml")})
    assert resp.status_code == 200
    check_workout_json(resp.json())
