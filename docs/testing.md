# Testing CRC and Property Cases

## Negative CRC Case Files
- Use files like tests/data/bad_crc.fit to test CRC failure.
- CLI/API should return non-zero exit and FitCRCError details.

## Property-based Testing
- Use Hypothesis to flip bits and test CRC robustness.
- Example:
  ```python
  from hypothesis import given, strategies as st
  @given(st.binary(min_size=100, max_size=1000))
  def test_crc_flip(data):
      # flip random bit, check CRC
      ...
  ```

See tests/test_fit_crc.py for examples.
