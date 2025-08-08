from ai_sport_agent.parsers.fit_parser import parse_fit
from tests.utils.fit_maker import make_fit_with_devfields
import math

def test_derived_fields(tmp_path):
    fit_path = tmp_path / "derived.fit"
    make_fit_with_devfields(fit_path)
    workout = parse_fit(fit_path)
    for rec in workout.records:
        if hasattr(rec, "speed_m_s") and rec.speed_m_s is not None:
            assert rec.speed_m_s >= 0
            if rec.speed_m_s > 0:
                assert rec.pace_s_km > 0
        if hasattr(rec, "grade_pct"):
            assert not (math.isnan(rec.grade_pct) or math.isinf(rec.grade_pct))
