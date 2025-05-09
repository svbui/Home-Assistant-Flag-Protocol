from datetime import datetime, timedelta, time

def calculate_easter(year: int) -> datetime:
    """Compute Easter Sunday for a given year (Anonymous Gregorian)."""
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
    day   = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day)

def nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> datetime:
    """
    Return the date of the nth `weekday` (0=Mon…6=Sun) in the given month.
    """
    dt = datetime(year, month, 1)
    # advance to first desired weekday
    offset = (weekday - dt.weekday()) % 7
    dt = dt + timedelta(days=offset)
    # advance (n-1) weeks
    dt = dt + timedelta(weeks=n-1)
    return dt

def last_weekday_of_month(year: int, month: int, weekday: int) -> datetime:
    """
    Return the date of the last `weekday` in the given month.
    """
    # start at last day
    from calendar import monthrange
    last_day = monthrange(year, month)[1]
    dt = datetime(year, month, last_day)
    offset = (dt.weekday() - weekday) % 7
    return dt - timedelta(days=offset)

def get_flag_status(now: datetime) -> tuple[str, str]:
    """Return (flag_type, reason) for Finland on this date/time."""
    year = now.year

    # 1) Fixed by law
    fixed = [
        (2, 28, "Kalevala Day / Day of Finnish Culture"),
        (5,  1, "Labour Day"),
        (6,  4, "Marshal Mannerheim’s Birthday / Defence Forces Flag Day"),
        (12, 6, "Independence Day"),
    ]

    # 2) Variable Sundays
    mothers = nth_weekday_of_month(year, 5, 6, 2)    # 2nd Sunday May
    fathers = nth_weekday_of_month(year,11, 6, 2)    # 2nd Sunday Nov
    remembrance = nth_weekday_of_month(year, 5, 6, 3) # 3rd Sunday May

    # 3) Midsummer Day: Saturday between 20–26 June
    midsummer = next(
        datetime(year, 6, d)
        for d in range(20, 27)
        if datetime(year, 6, d).weekday() == 5
    )

    # 4) Custom “established” days
    custom = [
        (2,  5, "Runeberg Day"),
        (3, 19, "Minna Canth Day / Equality Day"),
        (4,  9, "Finnish Language Day"),
        (4, 27, "National War Veterans’ Day"),
        (5,  9, "Europe Day"),
        (5, 12, "J. V. Snellman’s Birthday"),
        (7,  6, "Eino Leino Day / Poetry Celebration"),
        # Nature Day: last Saturday August
        # Miina Sillanpää Day: Oct 1
        # Aleksis Kivi Day: Oct 10
        # UN Day: Oct 24
        # Swedish Heritage Day: Nov 6
        # Children’s Rights Day: Nov 20
        # Sibelius Day: Dec 8
        (10, 1,  "Miina Sillanpää Day"),
        (10,10,  "Aleksis Kivi Day"),
        (10,24,  "United Nations Day"),
        (11, 6,  "Swedish Heritage Day"),
        (11,20,  "Children’s Rights Day"),
        (12, 8,  "Jean Sibelius Day"),
    ]

    # Determine the occasion
    occasion = None
    # fixed
    for m, d, reason in fixed:
        if now.month == m and now.day == d:
            occasion = reason
            break
    # mothers’ day
    if not occasion and now.date() == mothers.date():
        occasion = "Mother’s Day"
    # fathers’ day
    if not occasion and now.date() == fathers.date():
        occasion = "Father’s Day"
    # remembrance day
    if not occasion and now.date() == remembrance.date():
        occasion = "Remembrance Day"
    # midsummer
    if not occasion and now.date() == midsummer.date():
        occasion = "Midsummer Day"
    # custom list
    if not occasion:
        for m, d, reason in custom:
            if now.month == m and now.day == d:
                occasion = reason
                break

    # If no occasion today:
    if not occasion:
        return "no_flag", "No flag today"

    # Time window: hoist at 08:00, lower at sunset (handled by elevation) but no later than 21:00
    start = time(8, 0)
    end   = time(21, 0)
    if now.time() < start or now.time() > end:
        return "no_flag", f"Flag only {start.strftime('%H:%M')}–21:00"

    return "full_mast", occasion

def get_next_flag_day(now: datetime) -> tuple[int, str, str]:
    """Return (days_until, reason, flag_type) for the next Finnish flag day."""
    for i in range(1, 366):
        future_dt = now + timedelta(days=i)
        # use midday to avoid early/late time windows
        dt_mid = future_dt.replace(hour=12, minute=0, second=0, microsecond=0)
        flag_type, reason = get_flag_status(dt_mid)
        if flag_type != "no_flag":
            return i, reason, flag_type

    return -1, "Unknown", "no_flag"
