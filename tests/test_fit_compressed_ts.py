from ai_sport_agent.parsers.fit_parser import parse_fit
from tests.utils.fit_maker import make_compressed_ts_fit

def test_compressed_ts(tmp_path):
    fit_path = tmp_path / "compressed_ts.fit"
    make_compressed_ts_fit(fit_path)
    workout = parse_fit(fit_path)
    ts_list = [rec.timestamp for rec in workout.records if rec.timestamp]
    assert all(ts_list[i] < ts_list[i+1] for i in range(len(ts_list)-1))
