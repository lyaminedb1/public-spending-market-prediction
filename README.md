# public-spending-market-prediction

Do US federal contract awards move the stocks of the companies that win them, and can
you trade that?

The pipeline pulls every contract action of at least $7.5M from USAspending.gov. That
is the threshold above which the DoD publicly announces awards each evening. It maps
each recipient to a listed ticker and measures the abnormal stock return around the
announcement. It then learns which awards move prices and backtests a market-hedged
strategy on out-of-sample years only.

```
awards (USAspending) ─┐
                      ├─> firm-day events ─> market-model event study ─> features
prices (Yahoo/Stooq) ─┘                                                     │
                                  walk-forward models (size rule, ridge, GBM)
                                                                            │
                                     hedged 5-day event backtest ─> REPORT.md + charts
```

## Run it

```bash
pip install -e .[dev]

psmp run                    # synthetic data, runs anywhere (~15s)
psmp run --source live      # real data: needs api.usaspending.gov + query1.finance.yahoo.com
psmp sweep --seeds 20       # 80 synthetic worlds across 4 effect sizes, in parallel
pytest
```

Outputs go to `results/`: `REPORT.md`, charts, `summary.json`, and per-year model
metrics. The sweep writes `results/sweep/SWEEP.md`.

## Data sources

| source | what | notes |
|---|---|---|
| `live` | USAspending `spending_by_transaction` + Yahoo chart API (Stooq fallback), SPY as market | cached in `data/cache/`; `Mod == 0` marks a new award |
| `synthetic` | 28 real tickers, 11 years of fat-tailed returns with vol regimes, awards with a **known** injected effect | used to check that the pipeline finds a signal when one exists and nothing when none does |

## Method

- **Event:** all awards to one firm on one day, collapsed into one event. Day 0 is the
  first trading day on or after the action date. DoD announcements come after the
  close, so trading starts earning on day +1.
- **Abnormal returns:** market model fit on days −250..−21. The report shows the mean
  CAR, cross-sectional t, Patell z, a sign test and CAAR paths with 95% bands.
- **Features** (known at the day-0 close): award $ / market cap (total, max, new-award
  only), number of awards, new vs modification, competed share, DoD share, size,
  run-up on days −2..0, the day-0 reaction, 60-day momentum, beta, residual vol,
  recent award flow, surprise versus the firm's own history, and sector.
- **Models:** walk-forward by calendar year, purged at the train/test boundary. The
  entry threshold for each year comes from training-set predictions only.
- **Backtest:** long the stock, short beta × market, hold 5 days, equal weight across
  open positions, 10 bps per side.

## Layout

```
psmp/
  universe.py       tickers, market caps, recipient-name aliases + matcher
  data/live.py      USAspending + price fetchers with caching
  data/synthetic.py synthetic world with ground truth
  event_study.py    events, abnormal returns, CAAR, test statistics
  features.py       per-event features
  model.py          walk-forward models
  backtest.py       hedged event backtest
  report.py         charts + markdown helpers
  pipeline.py       end-to-end run
  sweep.py          multi-seed robustness sweep
tests/
```
