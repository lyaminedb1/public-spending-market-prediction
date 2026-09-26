"""Synthetic awards and prices with a known, injected award effect.

Used when the live APIs are unreachable and to check that the pipeline recovers
an effect it is told exists. The generator is deliberately noisy: fat-tailed
returns, volatility regimes, overlapping events, partial pre-announcement
leakage, and an effect that is only weakly tied to the observable features.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import AWARD_COLUMNS, MARKET
from ..universe import UNIVERSE

AGENCIES = (
    ("Department of Defense", 0.72, 1.0),
    ("Department of Health and Human Services", 0.08, 0.7),
    ("Department of Veterans Affairs", 0.06, 0.7),
    ("National Aeronautics and Space Administration", 0.05, 0.8),
    ("Department of Homeland Security", 0.05, 0.8),
    ("Department of Energy", 0.04, 0.6),
)

# How the post-announcement effect is spread over trading days +1..+5.
POST_PROFILE = np.array([0.55, 0.22, 0.10, 0.08, 0.05])


def generate(
    start: str = "2015-01-01",
    end: str = "2025-12-31",
    awards_per_year_scale: float = 1.0,
    effect_scale: float = 0.3,
    seed: int = 7,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """Return (awards, prices, true_post_effect indexed by award_id)."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start, end)
    n = len(dates)

    # Market: two volatility regimes with persistent switching, t(5) shocks.
    calm, stressed = 0.008, 0.02
    regime = np.zeros(n, dtype=int)
    for i in range(1, n):
        stay = 0.99 if regime[i - 1] == 0 else 0.95
        regime[i] = regime[i - 1] if rng.random() < stay else 1 - regime[i - 1]
    mkt_vol = np.where(regime == 0, calm, stressed)
    mkt_ret = 0.0003 + mkt_vol * rng.standard_t(5, n) / np.sqrt(5 / 3)

    returns = {MARKET: mkt_ret}
    award_rows = []
    truth = {}
    agency_names = [a[0] for a in AGENCIES]
    agency_p = np.array([a[1] for a in AGENCIES])
    agency_mult = {a[0]: a[2] for a in AGENCIES}

    for company in UNIVERSE:
        cap = company.market_cap_bn * 1e9
        beta = rng.uniform(0.6, 1.25)
        idio_vol = 0.011 + 0.012 / np.sqrt(company.market_cap_bn / 5)
        idio = idio_vol * rng.standard_t(4, n) / np.sqrt(2)
        r = beta * mkt_ret + idio

        years = n / 252
        rate = awards_per_year_scale * 12 * company.market_cap_bn ** 0.45
        n_awards = rng.poisson(rate * years)
        # Leave room for an estimation window before the first event and a
        # holding window after the last one.
        idx = np.sort(rng.integers(260, n - 25, n_awards))

        for k, i in enumerate(idx):
            amount = max(7.5e6, float(np.exp(rng.normal(np.log(3.5e7), 1.5))))
            # Very large awards go disproportionately to large primes.
            if company.market_cap_bn > 50 and rng.random() < 0.05:
                amount *= rng.uniform(5, 40)
            is_new = rng.random() < 0.35
            competed = rng.random() < 0.6
            agency = agency_names[rng.choice(len(AGENCIES), p=agency_p)]
            surprise = amount / cap

            effect = 1.8 * surprise
            effect *= 1.0 if is_new else 0.35
            effect *= 1.3 if competed else 0.8
            effect *= agency_mult[agency]
            effect *= float(np.exp(rng.normal(0, 0.6)))  # unobservable noise
            effect = min(effect, 0.08) * effect_scale
            # A slice of awards is disappointing news (e.g. smaller than rumored).
            if rng.random() < 0.15:
                effect = -0.5 * effect

            leaked = rng.random() < 0.2
            pre_share = rng.uniform(0.6, 1.0) if leaked else rng.uniform(0.0, 0.15)
            pre = effect * pre_share
            post = effect - pre
            # Pre-announcement drift on days -2..0, post on +1..+5.
            for d, w in zip((-2, -1, 0), (0.25, 0.35, 0.4)):
                if 0 <= i + d < n:
                    r[i + d] += pre * w
            for d, w in enumerate(POST_PROFILE, start=1):
                if i + d < n:
                    r[i + d] += post * w

            award_id = f"{company.ticker}-{k:05d}"
            truth[award_id] = post
            award_rows.append(
                {
                    "award_id": award_id,
                    "ticker": company.ticker,
                    "recipient_name": company.aliases[0] + " CORPORATION",
                    "amount": round(amount, 2),
                    "agency": agency,
                    "announce_date": dates[i],
                    "is_new": is_new,
                    "competed": competed,
                }
            )
        returns[company.ticker] = r

    ret = pd.DataFrame(returns, index=dates)
    prices = 100 * (1 + ret).cumprod()
    awards = (
        pd.DataFrame(award_rows, columns=AWARD_COLUMNS)
        .sort_values(["announce_date", "award_id"])
        .reset_index(drop=True)
    )
    return awards, prices, pd.Series(truth, name="true_post_effect")
