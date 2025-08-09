smoke:
	fitparser export tests/data/mini.gpx --json examples/json/workout_mini_run.json
	fitparser export tests/data/mini.tcx --json examples/json/workout_mini_bike.json
	fitparser validate tests/data/good.fit
	- fitparser validate tests/data/bad_crc.fit

quality-gates:
	pytest -q
	fitparser validate tests/data/good.fit
	- fitparser validate tests/data/bad_crc.fit
