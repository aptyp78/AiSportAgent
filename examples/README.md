# Examples for AiSportAgent

This folder contains sample files for testing and demonstration:

- `json/`: Example workouts in unified JSON format (see [schema/workout.schema.json](../schema/workout.schema.json))
- `csv/`: Lap summaries and record slices for quick analysis in Pandas
- `api/`: Example curl scripts for API usage

## How to generate

Use CLI:

```sh
ai_sport_agent export Data/RunGarminNoPower.fit --json examples/json/workout_mini_run.json
ai_sport_agent export Data/RunGarminNoPower.fit --json examples/json/workout_mini_bike.json
```

See [docs/examples.md](../docs/examples.md) for details and usage in Pandas.

# Examples Directory

## How to Generate JSON/CSV
- Use CLI:
  ```bash
  fitparser export tests/data/mini.gpx --json examples/json/workout_mini_run.json
  fitparser export tests/data/mini.tcx --json examples/json/workout_mini_bike.json
  ```
- See schema in `schema/workout.schema.json`.

## API Scripts
- Validate FIT CRC:
  ```bash
  bash examples/api/curl_validate_fit.sh
  ```
- Parse GPX:
  ```bash
  bash examples/api/curl_parse_gpx.sh
  ```

## CSV/JSON Fragments
- See `examples/csv/` and `examples/json/` for sample output.
