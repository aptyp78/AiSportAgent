"""Typer CLI for FIT file operations."""

import typer
from pathlib import Path
import json
import sys
from pydantic import ValidationError
from ai_sport_agent.core.models import Workout

app = typer.Typer(help="AI Sport Agent CLI")
@app.command()
def schema(out: Path = typer.Option(None, "--out", help="Output file for schema")):
    """Show or save JSON Schema for Workout."""
    schema = Workout.model_json_schema()
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(schema, indent=2))
        typer.echo(f"Schema saved to {out}")
    else:
        typer.echo(json.dumps(schema, indent=2))

@app.command()
def validate(json_file: Path):
    """Validate JSON file against Workout schema."""
    try:
        data = json.loads(json_file.read_text())
        Workout.model_validate(data)
        typer.echo("Valid: True")
        raise typer.Exit(code=0)
    except ValidationError as e:
        typer.echo(f"Valid: False\nErrors: {e.errors()}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

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
