"""Listed companies that win federal contracts, with the recipient-name aliases
USAspending uses for them.

Market caps are rough (USD billions) and only used to scale award sizes; the live
pipeline replaces them with nothing more precise than this, so treat the
"award / market cap" feature as an order-of-magnitude surprise measure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Company:
    ticker: str
    name: str
    sector: str
    market_cap_bn: float
    aliases: tuple[str, ...] = field(default_factory=tuple)


UNIVERSE: tuple[Company, ...] = (
    Company("LMT", "Lockheed Martin", "defense", 110, ("LOCKHEED MARTIN",)),
    Company("RTX", "RTX Corp", "defense", 150, ("RAYTHEON", "RTX CORPORATION", "PRATT & WHITNEY", "COLLINS AEROSPACE")),
    Company("GD", "General Dynamics", "defense", 75, ("GENERAL DYNAMICS", "ELECTRIC BOAT", "GULFSTREAM")),
    Company("NOC", "Northrop Grumman", "defense", 70, ("NORTHROP GRUMMAN",)),
    Company("BA", "Boeing", "defense", 120, ("BOEING",)),
    Company("LHX", "L3Harris", "defense", 45, ("L3HARRIS", "HARRIS CORPORATION", "L-3 COMMUNICATIONS", "AEROJET ROCKETDYNE")),
    Company("HII", "Huntington Ingalls", "defense", 10, ("HUNTINGTON INGALLS",)),
    Company("TXT", "Textron", "defense", 15, ("TEXTRON", "BELL TEXTRON", "BELL HELICOPTER")),
    Company("LDOS", "Leidos", "services", 20, ("LEIDOS",)),
    Company("BAH", "Booz Allen Hamilton", "services", 18, ("BOOZ ALLEN HAMILTON",)),
    Company("SAIC", "Science Applications Intl", "services", 6, ("SCIENCE APPLICATIONS INTERNATIONAL",)),
    Company("CACI", "CACI International", "services", 10, ("CACI",)),
    Company("PSN", "Parsons", "services", 8, ("PARSONS GOVERNMENT SERVICES", "PARSONS CORPORATION")),
    Company("KBR", "KBR", "services", 8, ("KBR",)),
    Company("MANT", "ManTech", "services", 4, ("MANTECH",)),
    Company("V2X", "V2X", "services", 1.5, ("VECTRUS", "V2X",)),
    Company("KTOS", "Kratos Defense", "defense", 4, ("KRATOS",)),
    Company("AVAV", "AeroVironment", "defense", 5, ("AEROVIRONMENT",)),
    Company("MRCY", "Mercury Systems", "defense", 2.5, ("MERCURY SYSTEMS",)),
    Company("PLTR", "Palantir", "tech", 60, ("PALANTIR",)),
    Company("MCK", "McKesson", "health", 70, ("MCKESSON",)),
    Company("CNC", "Centene", "health", 35, ("CENTENE", "HEALTH NET FEDERAL SERVICES")),
    Company("HUM", "Humana", "health", 40, ("HUMANA MILITARY", "HUMANA")),
    Company("FLR", "Fluor", "infrastructure", 7, ("FLUOR",)),
    Company("J", "Jacobs Solutions", "infrastructure", 17, ("JACOBS ENGINEERING", "JACOBS TECHNOLOGY")),
    Company("ACM", "AECOM", "infrastructure", 13, ("AECOM",)),
    Company("GE", "General Electric", "defense", 150, ("GENERAL ELECTRIC",)),
    Company("HON", "Honeywell", "defense", 130, ("HONEYWELL",)),
)

BY_TICKER = {c.ticker: c for c in UNIVERSE}

_SUFFIXES = re.compile(
    r"\b(INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LLC|L\.L\.C|LP|LTD|THE|HOLDINGS|GROUP)\b\.?"
)


def normalize_name(name: str) -> str:
    """Uppercase, strip punctuation and legal suffixes."""
    s = name.upper().replace(",", " ").replace(".", " ")
    s = _SUFFIXES.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def match_ticker(recipient_name: str) -> str | None:
    """Map a USAspending recipient name to a ticker, or None if not in the universe.

    Longest alias wins so "HUMANA MILITARY" beats "HUMANA".
    """
    norm = normalize_name(recipient_name)
    best: tuple[int, str] | None = None
    for c in UNIVERSE:
        for alias in c.aliases:
            a = normalize_name(alias)
            if a and re.search(rf"(^|\s){re.escape(a)}(\s|$)", norm):
                if best is None or len(a) > best[0]:
                    best = (len(a), c.ticker)
    return best[1] if best else None
