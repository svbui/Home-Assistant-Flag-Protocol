# custom_components/flag_protocol/flag_rules/is.py

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

def _time_window_check(now: datetime, flag_type: str, reason: str) -> tuple[str, str]:
    """
    Enforce Iceland’s time window:
      - Not before 07:00
      - Not after sunset (handled by elevation in sensor) or midnight
    """
    if now.time() < time(7, 0):
        return "no_flag", f"Flags not before 07:00 ({reason})"
    # No later than midnight
    if now.time() >= time(23, 59, 59):
        return "no_flag", f"Too late to fly flag ({reason})"
    return flag_type, reason

def get_flag_status(now: datetime) -> tuple[str, str]:
    """
    Iceland flag rules:
      - Full mast on fixed/variable dates (with reason)
      - Half mast on Good Friday
      - Time window enforced by _time_window_check()
    """
    year = now.year
    easter = calculate_easter(year)
    whit_sunday = easter + timedelta(days=49)

    # Variable dates
    # First Day of Summer: last Thursday in April
    for d in range(30, 22, -1):
        dt = datetime(year, 4, d)
        if dt.weekday() == 3:  # Thursday
            first_day_of_summer = dt
            break

    # Seamen's Day: first Sunday in June
    for d in range(1, 8):
        dt = datetime(year, 6, d)
        if dt.weekday() == 6:  # Sunday
            seamens_day = dt
            break

    # Fixed flag days
    fixed = {
        (1, 1):     "New Year's Day",
        (4, first_day_of_summer.day): "First Day of Summer",
        (5, 1):     "May Day",
        (6, seamens_day.day):         "Seamen's Day",
        (6, 17):    "National Day",
        (11, 16):   "Jónas Hallgrímsson's Birthday",
        (12, 1):    "Home Rule Day",
        (12, 25):   "Christmas Day",
    }

    # Check fixed dates
    key = (now.month, now.day)
    if key in fixed:
        return _time_window_check(now, "full_mast", fixed[key])

    # Good Friday: two days before Easter
    good_friday = easter - timedelta(days=2)
    if now.date() == good_friday.date():
        return _time_window_check(now, "half_mast", "Good Friday")

    # Easter Sunday
    if now.date() == easter.date():
        return _time_window_check(now, "full_mast", "Easter Sunday")

    # Whit Sunday (Pentecost)
    if now.date() == whit_sunday.date():
        return _time_window_check(now, "full_mast", "Whit Sunday")

    # No flag today
    return "no_flag", "No flag today"

def get_next_flag_day(now: datetime) -> tuple[int, str, str]:
    """
    Return (days_until, reason, flag_type) for the next Icelandic flag day.
    Uses a midday timestamp to avoid time-window misses.
    """
    for i in range(1, 366):
        future = now + timedelta(days=i)
        dt_mid = future.replace(hour=12, minute=0, second=0, microsecond=0)
        flag_type, reason = get_flag_status(dt_mid)
        if flag_type != "no_flag":
            return i, reason, flag_type
    return -1, "Unknown", "no_flag"
