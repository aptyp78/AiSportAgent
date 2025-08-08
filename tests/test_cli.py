import subprocess
import sys
from pathlib import Path

def test_cli_exists_and_help():
    result = subprocess.run([sys.executable, "-m", "ai_sport_agent.cli", "--help"], capture_output=True)
    assert result.returncode == 0
    assert b"Usage" in result.stdout or b"usage" in result.stdout

def test_cli_ingest_inspect_export(tmp_path):
    fit_file = tmp_path / "minimal.fit"
    fit_file.write_bytes(bytes([12]) + bytes(11))
    # ingest
    result = subprocess.run([sys.executable, "-m", "ai_sport_agent.cli", "ingest", str(tmp_path)], capture_output=True)
    assert result.returncode == 0
    # inspect
    result = subprocess.run([sys.executable, "-m", "ai_sport_agent.cli", "inspect", str(fit_file)], capture_output=True)
    assert result.returncode == 0
    # export
    out_json = tmp_path / "out.json"
    result = subprocess.run([sys.executable, "-m", "ai_sport_agent.cli", "export", str(fit_file), "--json", str(out_json)], capture_output=True)
    assert result.returncode == 0
    assert out_json.exists()
