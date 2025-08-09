# Examples: Workout, Lap, Record, Developer Fields

## Mini Workout JSON
See `examples/json/workout_mini_run.json` and `workout_mini_bike.json` for minimal workout structure.

## CSV Fragments
See `examples/csv/lap_summary.csv` and `record_slice.csv` for lap/record slices.

## API Scripts
- `examples/api/curl_validate_fit.sh`: Validate FIT file CRC via API.
- `examples/api/curl_parse_gpx.sh`: Parse GPX file via API.

## Developer/Derived Fields
- Developer fields: custom fields in FIT, see schema/workout.schema.json.
- Derived fields: calculated fields, see docs and Pandas usage.

## Pandas Usage
```python
import pandas as pd
records = pd.read_json('examples/json/workout_mini_run.json')['records']
```

## JSON Schema
See `schema/workout.schema.json` for full model.

# Examples

## JSON: Workout
```json
{
  "header": {"protocol": 0, "profile": 0},
  "records": [{"timestamp": 1717262400, "distance_m": 0, "power": 210, "hr_bpm": 120}],
  "laps": [{"start": 1717262400, "end": 1717262700, "distance_m": 500}],
  "events": [],
  "schema_version": "1.0.0"
}
```

## CSV: Lap summary
```
lap_idx,start_time,end_time,distance_m,avg_power_w,avg_hr_bpm,moving_time_s
0,1717262400,1717262700,500,212,121,300
```

## CSV: Record slice
```
timestamp,distance_m,power,hr_bpm,cadence_rpm,speed_m_s,position_lat,position_long
1717262400,0,210,120,,3.33,55.0,37.0
1717262410,33,215,122,,3.39,55.0001,37.0001
```

## API usage in Pandas
```python
import pandas as pd
records = pd.read_json('examples/json/workout_mini_run.json')['records']
laps = pd.read_json('examples/json/workout_mini_run.json')['laps']
```

## Developer fields & derived
- `developer_fields`: custom sensor data (e.g. Stryd power)
- `speed_m_s`, `pace_s_km`, `grade_pct`: calculated fields, can be disabled via CLI/API
