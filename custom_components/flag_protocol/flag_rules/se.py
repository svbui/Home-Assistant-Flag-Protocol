from datetime import datetime, timedelta, time

def calculate_easter(year: int) -> datetime:
    """Compute Easter Sunday for a given year (Anonymous Gregorian algorithm)."""
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
    """Return (flag_type, reason) for Sweden for this datetime."""
    year = now.year
    easter = calculate_easter(year)
    whit = easter + timedelta(days=49)
    midsummer = next(
        datetime(year, 6, d)
        for d in range(20, 27)
        if datetime(year, 6, d).weekday() == 5
    )

    fixed = [
        (1, 1,   "New Year's Day"),
        (1, 28,  "King’s Name Day"),
        (3, 12,  "Crown Princess’s Name Day"),
        (4, 30,  "King’s Birthday"),
        (5, 1,   "First of May"),
        (5, 29,  "Veterans Day"),
        (6, 6,   "National Day"),
        (7, 14,  "Princess’s Birthday"),
        (8, 8,   "Queen’s Name Day"),
        (10, 24, "UN Day"),
        (11, 6,  "Gustav II Adolf Day"),
        (12, 10, "Nobel Day"),
        (12, 23, "Queen’s Birthday"),
        (12, 25, "Christmas Day")
    ]

    # Determine reason
    if (now.month, now.day) in {(m, d) for m, d, _ in fixed}:
        reason = next(r for m, d, r in fixed if m == now.month and d == now.day)
    elif now.date() == easter.date():
        reason = "Easter Sunday"
    elif now.date() == whit.date():
        reason = "Whit Sunday"
    elif now.date() == midsummer.date():
        reason = "Midsummer Day"
    else:
        return "no_flag", "No flag today"

    # Time‐based visibility: Mar–Oct from 08:00, Nov–Feb from 09:00; until 21:00
    start = time(9) if now.month in (11, 12, 1, 2) else time(8)
    end = time(21, 0)
    if not (start <= now.time() <= end):
        return "no_flag", f"Flag only {start.strftime('%H:%M')}-21:00"

    return "full_mast", reason


def get_next_flag_day(now: datetime) -> tuple[int, str, str]:
    """Return (days_until, reason, flag_type) for next Swedish flag day, ignoring current time-of-day."""
    for i in range(1, 366):
        future_date = now.date() + timedelta(days=i)
        # Use a midday time to ensure within visibility window for search
        dt = datetime(future_date.year, future_date.month, future_date.day, 12, 0)
        flag_type, reason = get_flag_status(dt)
        if flag_type != "no_flag":
            return i, reason, flag_type
    return -1, "Unknown", "no_flag"
