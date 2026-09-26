"""Data sources.

Every source returns the same two frames:

awards: one row per contract action, columns
    award_id, ticker, recipient_name, amount, agency, announce_date, is_new, competed
prices: adjusted closes indexed by trading date, one column per ticker plus "MKT"
"""

AWARD_COLUMNS = [
    "award_id",
    "ticker",
    "recipient_name",
    "amount",
    "agency",
    "announce_date",
    "is_new",
    "competed",
]

MARKET = "MKT"
