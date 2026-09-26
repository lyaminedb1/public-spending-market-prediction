import numpy as np
import pandas as pd
import pytest

from psmp import backtest
from psmp.data import MARKET
from psmp.data.synthetic import generate
from psmp.event_study import abnormal_returns, build_events, car
from psmp.features import FEATURES, build_features
from psmp.pipeline import run


@pytest.fixture(scope="module")
def world():
    return generate("2016-01-01", "2020-12-31", awards_per_year_scale=0.5, effect_scale=1.0, seed=1)


def test_build_events_collapses_same_day_awards():
    days = pd.bdate_range("2020-01-01", periods=10)
    awards = pd.DataFrame(
        {
            "award_id": ["a", "b", "c"],
            "ticker": ["LMT", "LMT", "LMT"],
            "recipient_name": ["x"] * 3,
            "amount": [10e6, 20e6, 5e6],
            "agency": ["Department of Defense"] * 3,
            # Saturday rolls to Monday and merges with Monday's award.
            "announce_date": [pd.Timestamp("2020-01-04"), pd.Timestamp("2020-01-06"), days[0]],
            "is_new": [True, False, False],
            "competed": [True, False, pd.NA],
        }
    )
    ev = build_events(awards, days)
    assert len(ev) == 2
    monday = ev[ev["day0"] == pd.Timestamp("2020-01-06")].iloc[0]
    assert monday["amount"] == 30e6
    assert monday["n_awards"] == 2
    assert monday["new_amount"] == 10e6
    assert bool(monday["any_new"])


def test_abnormal_returns_zero_for_pure_market_stock():
    days = pd.bdate_range("2018-01-01", periods=400)
    rng = np.random.default_rng(0)
    m = rng.normal(0, 0.01, len(days))
    prices = pd.DataFrame(
        {MARKET: 100 * np.cumprod(1 + m), "LMT": 50 * np.cumprod(1 + 0.001 + 1.5 * m)}, index=days
    )
    events = pd.DataFrame({"ticker": ["LMT"], "day0_idx": [300]})
    ar = abnormal_returns(events, prices)
    assert ar["beta"].iloc[0] == pytest.approx(1.5, abs=1e-6)
    cols = [c for c in ar.columns if c.startswith("ar")]
    assert np.abs(ar[cols].to_numpy()).max() < 1e-9


def test_event_study_recovers_injected_effect(world):
    awards, prices, truth = world
    ev = build_events(awards, prices.index)
    ar = abnormal_returns(ev, prices)
    post = car(ar, 1, 5)
    true_post = ev["award_ids"].map(lambda ids: sum(truth[i] for i in ids))
    ok = post.notna()
    assert post[ok].mean() == pytest.approx(true_post[ok].mean(), abs=0.002)
    assert post[ok].mean() > 0


def test_features_use_only_past_information(world):
    awards, prices, _ = world
    ev = build_events(awards, prices.index)
    ar = abnormal_returns(ev, prices)
    X = build_features(ev, ar, prices)
    assert list(X.columns) == FEATURES
    # Post-event returns must not leak in: shuffling them leaves features unchanged.
    ar2 = ar.copy()
    post_cols = [f"ar+{d}" for d in range(1, 21)]
    ar2[post_cols] = ar2[post_cols].sample(frac=1, random_state=0).to_numpy()
    pd.testing.assert_frame_equal(X, build_features(ev, ar2, prices))


def test_backtest_charges_costs_and_is_flat_without_trades(world):
    awards, prices, _ = world
    ev = build_events(awards, prices.index)
    ev = ev.join(abnormal_returns(ev, prices)[["beta"]])
    none = backtest.run(ev, pd.Series(False, index=ev.index), prices)
    assert none["stats"]["trades"] == 0
    some = ev.index[:50]
    sel = pd.Series(ev.index.isin(some), index=ev.index)
    cheap = backtest.run(ev, sel, prices, cost_bps=0)
    dear = backtest.run(ev, sel, prices, cost_bps=50)
    assert dear["stats"]["avg_trade"] < cheap["stats"]["avg_trade"]


def test_full_run_smoke(tmp_path):
    s = run(source="synthetic", start="2015-01-01", end="2020-12-31", first_test_year=2018,
            out_dir=str(tmp_path), scale=0.5, effect_scale=1.0)
    assert (tmp_path / "REPORT.md").exists()
    assert (tmp_path / "equity.png").exists()
    assert set(s["backtests"]) >= {"all awards", "size_rule", "ridge", "gbm", "random 20%"}
    assert s["synthetic_validation"]["ic_vs_truth_size_rule"] > 0.3
