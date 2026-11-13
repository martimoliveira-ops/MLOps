---
applyTo: 'tests/**/*.py'
---

- Name files `tests/test_<module>.py`. Name tests after the behaviour they check, for example `test_lag_features_use_only_past_values`.
- Never load the full dataset. Use the small hand-made files in `tests/fixtures/`.
- Every new feature function needs a test that proves it uses no future data.
- Keep one behaviour per test, with a clear arrange, act and assert.
- A test should fail without the change it covers. Check that before calling it done.
