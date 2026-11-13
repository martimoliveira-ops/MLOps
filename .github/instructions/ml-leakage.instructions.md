---
applyTo: 'src/forecaster/**/*.py,notebooks/**/*.ipynb'
---

These rules come from the Phase 1 findings. Breaking them gives models that look right and are wrong.

- The forecast is made at midnight of day D for all 24 hours of day D+1. Every feature must be known at midnight of day D.
- A lag must be at least 24 hours before the hour it predicts.
- Split and backtest by time only, with expanding or rolling windows. Never shuffle, and never use a random split such as `train_test_split` with its default shuffle.
- Data after the cut-off date in `params.yaml` (about 30 June 2014) is never used for training, tuning or backtesting in Phases 2 and 3.
- Compare every model with both seasonal-naive baselines (daily and weekly) on MAE, MAPE and euro cost, with a Diebold-Mariano test behind any claimed difference.
- Zeros before a client's first reading mean "not a client yet". Treat them as missing, not as zero consumption.
