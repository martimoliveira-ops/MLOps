---
applyTo: 'src/**/*.py'
---

- Write small, pure functions that take and return DataFrames or Series. They are the easiest to test.
- Keep I/O (S3, files, environment variables) at the edges, in their own functions.
- Format with black. Keep pylint clean: the Makefile runs it with `--disable=R,C`.
- Timestamps mark the end of each 15-minute interval. Resample with `label="right", closed="right"`.
- Units: values are the average kW over 15 minutes. kWh = value / 4. Hourly energy is the sum of four kWh values.
- Daylight saving time is in the values, not the index. The index is a regular 15-minute wall-clock grid.
