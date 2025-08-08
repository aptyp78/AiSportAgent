"""Typer CLI for FIT file operations."""

import typer
from pathlib import Path
import json
from ai_sport_agent.parsers.base_parser import StubParser

app = typer.Typer(help="AI Sport Agent CLI")

@app.command()
def ingest(path: Path):
    """Count FIT files in path and print summary."""
    files = list(path.rglob("*.fit")) if path.is_dir() else [path]
    typer.echo(f"Found {len(files)} FIT files.")

@app.command()
def inspect(file: Path):
    """Print basic file metadata."""
    if not file.exists():
        typer.echo("File not found.", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"File: {file.name}, Size: {file.stat().st_size} bytes")

@app.command()
def export(file: Path, json_out: Path = typer.Option(..., "--json")):
    """Export parsed FIT file to JSON."""
    parser = StubParser()
    workout = parser.parse(file)
    with json_out.open("w") as f:
        json.dump({"laps": [lap.dict() for lap in workout.laps], "events": [ev.dict() for ev in workout.events]}, f)
    typer.echo(f"Exported to {json_out}")

if __name__ == "__main__":
    app()
