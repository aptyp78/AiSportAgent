"""Base FIT parser and stub implementation."""

from pathlib import Path
from ai_sport_agent.core.models import Workout

class BaseParser:
    def parse(self, file: Path) -> Workout:
        """Parse FIT file and return Workout model."""
        raise NotImplementedError

class StubParser(BaseParser):
    def parse(self, file: Path) -> Workout:
        """Stub parser for testing."""
        return Workout(
            header={"protocol": 0, "profile": 0},
            records=[],
            laps=[],
            events=[]
        )
