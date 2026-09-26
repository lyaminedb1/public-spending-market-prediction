"""Live data: contract transactions from USAspending.gov and prices from Yahoo/Stooq.

Needs outbound access to api.usaspending.gov and query1.finance.yahoo.com (or
stooq.com). Responses are cached under data/cache so reruns are offline.
"""

from __future__ import annotations

import hashlib
import io
import json
import time
from pathlib import Path

import pandas as pd
import requests

from . import AWARD_COLUMNS, MARKET
from ..universe import UNIVERSE, match_ticker

USASPENDING_URL = "https://api.usaspending.gov/api/v2/search/spending_by_transaction/"
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
STOOQ_URL = "https://stooq.com/q/d/l/?s={ticker}.us&i=d"
MARKET_PROXY = "SPY"
# The DoD publishes every contract action worth at least $7.5M the evening it is
# signed, which is what makes these awards tradable news.
MIN_AMOUNT = 7_500_000
CONTRACT_TYPES = ["A", "B", "C", "D"]
TX_FIELDS = [
    "Award ID",
    "Mod",
    "Recipient Name",
    "Action Date",
    "Transaction Amount",
    "Awarding Agency",
]

CACHE_DIR = Path("data/cache")
HEADERS = {"User-Agent": "psmp research (public-spending-market-prediction)"}


def _cached(key: str, fetch):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / (hashlib.sha1(key.encode()).hexdigest()[:16] + ".json")
    if path.exists():
        return json.loads(path.read_text())
    data = fetch()
    path.write_text(json.dumps(data))
    return data


def _post(url: str, body: dict, retries: int = 4) -> dict:
    for attempt in range(retries):
        try:
            r = requests.post(url, json=body, headers=HEADERS, timeout=60)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    raise AssertionError("unreachable")


def fetch_transactions(keyword: str, start: str, end: str, max_pages: int = 50) -> list[dict]:
    """All contract transactions >= MIN_AMOUNT whose recipient matches `keyword`."""
    rows: list[dict] = []
    for page in range(1, max_pages + 1):
        body = {
            "filters": {
                "award_type_codes": CONTRACT_TYPES,
                "recipient_search_text": [keyword],
                "time_period": [{"start_date": start, "end_date": end}],
                "award_amounts": [{"lower_bound": MIN_AMOUNT}],
            },
            "fields": TX_FIELDS,
            "sort": "Action Date",
            "order": "asc",
            "limit": 100,
            "page": page,
        }
        key = f"tx|{keyword}|{start}|{end}|{page}"
        data = _cached(key, lambda: _post(USASPENDING_URL, body))
        rows.extend(data.get("results", []))
        if not data.get("page_metadata", {}).get("hasNext"):
            break
    return rows


def load_awards(start: str, end: str) -> pd.DataFrame:
    records = []
    seen: set[tuple] = set()
    for company in UNIVERSE:
        for alias in company.aliases:
            for tx in fetch_transactions(alias, start, end):
                name = tx.get("Recipient Name") or ""
                ticker = match_ticker(name)
                if ticker != company.ticker:
                    continue
                key = (tx.get("Award ID"), tx.get("Mod"), tx.get("Action Date"))
                if key in seen:
                    continue
                seen.add(key)
                amount = float(tx.get("Transaction Amount") or 0)
                if amount < MIN_AMOUNT:
                    continue
                records.append(
                    {
                        "award_id": f"{tx.get('Award ID')}#{tx.get('Mod')}",
                        "ticker": ticker,
                        "recipient_name": name,
                        "amount": amount,
                        "agency": tx.get("Awarding Agency") or "UNKNOWN",
                        "announce_date": pd.Timestamp(tx.get("Action Date")),
                        "is_new": str(tx.get("Mod", "")).strip() in ("0", ""),
                        # The transaction endpoint does not expose extent-competed.
                        "competed": pd.NA,
                    }
                )
    df = pd.DataFrame.from_records(records, columns=AWARD_COLUMNS)
    return df.sort_values("announce_date").reset_index(drop=True)


def _yahoo(ticker: str, start: str, end: str) -> pd.Series:
    p1 = int(pd.Timestamp(start).timestamp())
    p2 = int(pd.Timestamp(end).timestamp())
    url = YAHOO_URL.format(ticker=ticker)

    def fetch():
        r = requests.get(
            url,
            params={"period1": p1, "period2": p2, "interval": "1d", "events": "div,split"},
            headers=HEADERS,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    data = _cached(f"yahoo|{ticker}|{start}|{end}", fetch)
    res = data["chart"]["result"][0]
    idx = pd.to_datetime(res["timestamp"], unit="s").normalize()
    close = res["indicators"]["adjclose"][0]["adjclose"]
    return pd.Series(close, index=idx, name=ticker, dtype=float)


def _stooq(ticker: str, start: str, end: str) -> pd.Series:
    def fetch():
        r = requests.get(STOOQ_URL.format(ticker=ticker.lower()), headers=HEADERS, timeout=30)
        r.raise_for_status()
        return {"csv": r.text}

    text = _cached(f"stooq|{ticker}", fetch)["csv"]
    df = pd.read_csv(io.StringIO(text), parse_dates=["Date"]).set_index("Date")
    return df["Close"].loc[start:end].rename(ticker).astype(float)


def load_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    cols = {}
    for t in [MARKET_PROXY, *tickers]:
        try:
            s = _yahoo(t, start, end)
        except Exception:
            try:
                s = _stooq(t, start, end)
            except Exception as exc:  # delisted or unreachable ticker
                print(f"  price fetch failed for {t}: {exc}")
                continue
        cols[MARKET if t == MARKET_PROXY else t] = s
    prices = pd.DataFrame(cols).sort_index()
    prices = prices[~prices.index.duplicated()]
    return prices


def load(start: str = "2015-01-01", end: str = "2025-12-31") -> tuple[pd.DataFrame, pd.DataFrame]:
    awards = load_awards(start, end)
    prices = load_prices(sorted(awards["ticker"].unique()), start, end)
    return awards, prices
