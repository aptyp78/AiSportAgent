# API Reference

## POST /v1/validate

Validate FIT file CRC and schema.

### 200 OK
```json
{ "valid": true, "checks": { "crc": "pass", "schema": "pass" }, "meta": { "crc_checked": true } }
```

### 422 Unprocessable Entity
```json
{
  "valid": false,
  "checks": { "crc": "fail", "schema": "skip" },
  "errors": [{
    "type": "FitCRCError",
    "where": "data",
    "expected": "0x7B3A",
    "actual": "0x5C11",
    "offset": 1048576
  }]
}
```

See SRS and doc-package for endpoint structure and log format details.
