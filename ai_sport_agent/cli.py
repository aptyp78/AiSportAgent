"""Typer CLI for FIT file operations."""

import typer
from pathlib import Path
import json
def get_parser_for_file(file: Path):
    ext = file.suffix.lower()
    if ext == ".fit":
        from ai_sport_agent.parsers.fit_parser import parse_fit
        return parse_fit
    elif ext == ".gpx":
        from ai_sport_agent.parsers.gpx_parser import parse_gpx
        return parse_gpx
    elif ext == ".tcx":
        from ai_sport_agent.parsers.tcx_parser import parse_tcx
        return parse_tcx
    else:
        raise typer.Exit(code=1)

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
    """Export parsed file to JSON."""
    parser = get_parser_for_file(file)
    workout = parser(file)
    with json_out.open("w") as f:
        import json
        json.dump(workout.model_dump(), f, default=str)
    typer.echo(f"Exported to {json_out}")

if __name__ == "__main__":
    app()
