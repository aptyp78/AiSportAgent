"""FastAPI v1 endpoints for FIT parsing."""


from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from ai_sport_agent.parsers.base_parser import StubParser
from ai_sport_agent.parsers.fit_parser import parse_fit
from ai_sport_agent.parsers.errors import FitCRCError
from pydantic import ValidationError
from ai_sport_agent.core.models import Workout

app = FastAPI()

@app.post("/v1/validate")
async def validate(data: dict):
    try:
        Workout.model_validate(data)
        return {"valid": True, "errors": []}
    except ValidationError as e:
        return {"valid": False, "errors": e.errors()}

@app.post("/v1/validate-fit")
async def validate_fit(file: UploadFile = File(...)):
    try:
        # Сохраняем загруженный файл во временный путь
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        workout = parse_fit(Path(tmp_path))
        return {"valid": True, "workout": workout.dict()}
    except FitCRCError as e:
        return {
            "valid": False,
            "error": "FitCRCError",
            "details": {
                "where": e.details.get("where"),
                "expected": e.details.get("expected"),
                "actual": e.details.get("actual"),
                "offset": e.details.get("offset")
            }
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}

@app.get("/v1/health")
def health():
    return {"status": "ok"}

@app.post("/v1/parse")
async def parse(file: UploadFile = File(...)):
    parser = StubParser()
    # For stub, ignore file content
    workout = parser.parse(None)
    return {"laps": [lap.dict() for lap in workout.laps], "events": [ev.dict() for ev in workout.events]}
