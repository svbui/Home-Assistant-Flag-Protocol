# custom_components/flag_protocol/flag_rules/no.py

from datetime import datetime, timedelta, time

def calculate_easter(year: int) -> datetime:
    """Compute Easter Sunday for a given year (Gregorian algorithm)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day)

def get_flag_status(now: datetime) -> tuple[str, str]:
    """
    Norway flag rules (§4 & §6):
    - Fixed dates (full mast)
    - Easter Sunday & Whit Sunday (full mast)
    - Time window: Mar–Oct from 08:00, Nov–Feb from 09:00; haul at sunset or latest 21:00
    """
    year = now.year
    easter = calculate_easter(year)
    whit_sunday = easter + timedelta(days=49)

    # Fixed‐date national days
    fixed = [
        (1,  1,   "New Year's Day"),
        (1, 21,   "Princess Ingrid Alexandra’s Birthday"),
        (2,  5,   "Sami People's Day"),
        (2, 21,   "King Harald V’s Birthday"),
        (5,  1,   "Labour Day"),
        (5,  8,   "Liberation Day"),
        (5, 17,   "Constitution Day"),
        (6,  7,   "Union Dissolution Day (1905)"),
        (7,  4,   "Queen Sonja’s Birthday"),
        (7, 20,   "Crown Prince Haakon Magnus’s Birthday"),
        (7, 29,   "Olsok (St. Olav’s Day)"),
        (8, 19,   "Crown Princess Mette-Marit’s Birthday"),
        (12,25,   "Christmas Day"),
    ]

    # Determine if today is a flag day
    if (now.month, now.day) in {(m, d) for m, d, _ in fixed}:
        reason = next(r for m, d, r in fixed if m == now.month and d == now.day)
        flag_type = "full_mast"

    elif now.date() == easter.date():
        flag_type, reason = "full_mast", "Easter Sunday"

    elif now.date() == whit_sunday.date():
        flag_type, reason = "full_mast", "Whit Sunday"

    else:
        return "no_flag", "No flag today"

    # Time‐based visibility (§6)
    # Start: 09:00 in Nov–Feb, else 08:00
    start = time(9) if now.month in (11, 12, 1, 2) else time(8)
    # End by sunset or latest 21:00 (sunset handled at sensor level via elevation)
    end = time(21, 0)
    current = now.time()

    if not (start <= current <= end):
        return "no_flag", f"Flag only {start.strftime('%H:%M')}–21:00"

    return flag_type, reason

def get_next_flag_day(now: datetime) -> tuple[int, str, str]:
    """
    Look forward up to one year to find the next flag day,
    returning (days_until, reason, flag_type).
    Uses a midday timestamp to avoid time‐window misses.
    """
    for i in range(1, 366):
        future = now + timedelta(days=i)
        # Midday to bypass early/late time checks
        dt_mid = datetime(future.year, future.month, future.day, 12, 0)
        flag_type, reason = get_flag_status(dt_mid)
        if flag_type != "no_flag":
            return i, reason, flag_type

    return -1, "Unknown", "no_flag"
