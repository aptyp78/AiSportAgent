"""FastAPI v1 endpoints for FIT parsing."""

from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from ai_sport_agent.core.models import Workout

app = FastAPI()

@app.get("/v1/health")
def health():
    return {"status": "ok"}

@app.post("/v1/parse")
async def parse(file: UploadFile = File(...)):
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp.write(await file.read())
        tmp.flush()
        ext = Path(tmp.name).suffix.lower()
        if ext == ".fit":
            from ai_sport_agent.parsers.fit_parser import parse_fit
            parser = parse_fit
        elif ext == ".gpx":
            from ai_sport_agent.parsers.gpx_parser import parse_gpx
            parser = parse_gpx
        elif ext == ".tcx":
            from ai_sport_agent.parsers.tcx_parser import parse_tcx
            parser = parse_tcx
        else:
            return {"error": "Unsupported file type"}
        workout = parser(Path(tmp.name))
    return workout.model_dump()
