---
name: data-and-ml-rules
description: The data and forecasting rules for this repo, covering forecast timing, lags, time-based splits, the cut-off date, baselines, zeros and daylight saving. Load when writing or reviewing feature, split, backtest or evaluation code.
---

The source of truth is the "Data rules" section of AGENTS.md. Use this as the checklist while you write the code.

**Forecast timing**

- At midnight of day D, forecast all 24 hours of day D+1.
- Every feature for an hour must be known at midnight of day D. A lag is at least 24 hours before the hour it predicts.

**Splits and backtests**

- Split by time only. Never shuffle, never use a random split, never use plain KFold.
- Backtest with expanding or rolling windows. Each fold trains only on data before its test period.

**Cut-off**

- Data after the cut-off date in `params.yaml` (about 30 June 2014) is reserved for the simulated production period. It's never used for training, tuning or backtesting in Phases 2 and 3. Read the date from config, not from a hard-coded value.

**Data quirks**

- Timestamps mark the end of each interval. Resample with `label="right", closed="right"`.
- Values are the average kW over 15 minutes. kWh = value / 4. Hourly energy is the sum of four kWh values.
- The index is a regular 15-minute wall-clock grid. Daylight saving lives in the values: on the March change day, 1:00 to 2:00 is zero; on the October change day, one wall-clock hour holds two hours of consumption.
- Zeros before a client's first reading (or after it leaves) are missing, not zero consumption.

**Evaluation**

- Compare every model with both seasonal-naive baselines, daily and weekly, on MAE, MAPE and euro cost. Back any claimed difference with a Diebold-Mariano test.

**Tests**

- Every new feature function has a test that proves it uses no future data.
- Tests use the small files in `tests/fixtures/`, never the full dataset.

If you can't check a rule from the code and config alone, say which rule it is and what you'd need to check it.
