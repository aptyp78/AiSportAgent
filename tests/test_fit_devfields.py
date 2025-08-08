from ai_sport_agent.parsers.fit_parser import parse_fit
from tests.utils.fit_maker import make_fit_with_devfields

def test_fit_devfields(tmp_path):
    fit_path = tmp_path / "devfield.fit"
    make_fit_with_devfields(fit_path)
    workout = parse_fit(fit_path)
    assert workout.records
    rec = workout.records[0]
    assert rec.developer_fields is not None
    assert "dev_2" in rec.developer_fields
    assert rec.developer_fields["dev_2"] == 7
