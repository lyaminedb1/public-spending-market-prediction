from psmp.universe import match_ticker, normalize_name


def test_normalize_strips_suffixes():
    assert normalize_name("Lockheed Martin Corp.") == "LOCKHEED MARTIN"
    assert normalize_name("The Boeing Company") == "BOEING"


def test_match_known_recipients():
    assert match_ticker("LOCKHEED MARTIN CORPORATION") == "LMT"
    assert match_ticker("Raytheon Company") == "RTX"
    assert match_ticker("ELECTRIC BOAT CORPORATION") == "GD"
    assert match_ticker("HUNTINGTON INGALLS INCORPORATED") == "HII"


def test_longest_alias_wins_and_word_boundaries():
    assert match_ticker("HUMANA MILITARY HEALTHCARE SERVICES INC") == "HUM"
    # "KBR" must not match inside another word.
    assert match_ticker("AKBRIGHT SOLUTIONS LLC") is None
    assert match_ticker("Some Unlisted Contractor LLC") is None
