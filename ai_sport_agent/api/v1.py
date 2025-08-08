"""FastAPI v1 endpoints for FIT parsing."""

from fastapi import FastAPI, UploadFile, File
from ai_sport_agent.parsers.base_parser import StubParser
from ai_sport_agent.core.models import Workout

app = FastAPI()

@app.get("/v1/health")
def health():
    return {"status": "ok"}

@app.post("/v1/parse")
async def parse(file: UploadFile = File(...)):
    parser = StubParser()
    # For stub, ignore file content
    workout = parser.parse(None)
    return {"laps": [lap.dict() for lap in workout.laps], "events": [ev.dict() for ev in workout.events]}
