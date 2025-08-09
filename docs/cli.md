# CLI Reference

## fitparser validate <file.fit>
Validate FIT file CRC and schema.

- Returns exit code 0 for valid, 2 for CRC error, 1 for other errors.
- Example:
  ```bash
  fitparser validate tests/data/good.fit
  fitparser validate tests/data/bad_crc.fit # exit code 2
  ```

## fitparser export/ingest --skip-crc
Export or ingest FIT file, skipping CRC validation.

- Example:
  ```bash
  fitparser export tests/data/good.fit --json out.json --skip-crc
  fitparser ingest tests/data/good.fit --skip-crc
  ```

See Makefile and examples/ for more usage.
