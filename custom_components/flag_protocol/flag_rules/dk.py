# custom_components/flag_protocol/flag_rules/dk.py

from datetime import datetime, timedelta, time
import calendar

def calculate_easter(year: int) -> datetime:
    """Compute Easter Sunday for a given year (Anonymous Gregorian)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day   = ((h + l - 7*m + 114) % 31) + 1
    return datetime(year, month, day)

def get_flag_status(now: datetime) -> tuple[str, str]:
    """
    Denmark flag rules:
      - Fixed dates (full mast), some half-mast conditions
      - Good Friday: half mast all day
      - Easter Sunday & Monday: full mast
      - Ascension Day: full mast
      - Whit Sunday (Pentecost): full mast
      - April 9: half mast until 12:00 (Occupation Day)
      - Only between 08:00 and sundown (sensor code enforces elevation > 3)
    """
    year = now.year
    easter = calculate_easter(year)
    good_friday    = easter - timedelta(days=2)
    easter_monday  = easter + timedelta(days=1)
    ascension      = easter + timedelta(days=39)
    whit_sunday    = easter + timedelta(days=49)

    fixed = [
        (1,  1,  "full_mast", "New Year's Day"),
        (2,  5,  "full_mast", "Crown Princess Mary's Birthday"),
        (2,  6,  "full_mast", "Princess Marie’s Birthday"),
        (4, 16,  "full_mast", "Queen Margrethe II’s Birthday"),
        (4, 29,  "full_mast", "Princess Benedikte’s Birthday"),
        (5,  5,  "full_mast", "Liberation Day"),
        (5, 26,  "full_mast", "Crown Prince Frederik’s Birthday"),
        (6,  5,  "full_mast", "Constitution Day"),
        (6,  7,  "full_mast", "Prince Joachim’s Birthday"),
        (6, 11,  "full_mast", "Prince Henrik’s Birthday"),
        (6, 15,  "full_mast", "Valdemars Day (Dannebrog)"),
        (9,  5,  "full_mast", "Commemoration of Danish Soldiers"),
        (12,25,  "full_mast", "Christmas Day"),
    ]

    # Half-mast special
    if now.date() == good_friday.date():
        flag_type, reason = "half_mast", "Good Friday"
    elif now.month == 4 and now.day == 9:
        # Occupation Day: half-mast until 12:00
        if now.time() < time(12, 0):
            flag_type, reason = "half_mast", "Occupation Day (half-mast until noon)"
        else:
            flag_type, reason = "full_mast", "Occupation Day"
    # Easter/Easter Monday/Ascension/Whit
    elif now.date() == easter.date():
        flag_type, reason = "full_mast", "Easter Sunday"
    elif now.date() == easter_monday.date():
        flag_type, reason = "full_mast", "Easter Monday"
    elif now.date() == ascension.date():
        flag_type, reason = "full_mast", "Ascension Day"
    elif now.date() == whit_sunday.date():
        flag_type, reason = "full_mast", "Whit Sunday"
    else:
        # Fixed date lookup
        for m, d, ftype, descr in fixed:
            if now.month == m and now.day == d:
                flag_type, reason = ftype, descr
                break
        else:
            return "no_flag", "No flag today"

    # Time window: not before 08:00
    if now.time() < time(8, 0):
        return "no_flag", "Flags only after 08:00"

    # Sun elevation check (sunrise/sundown) is handled by the core sensor logic:
    #   for Denmark, you might adjust sensor.py to use elevation > 0 instead of >3.

    return flag_type, reason

def get_next_flag_day(now: datetime) -> tuple[int, str, str]:
    """Loop ahead up to 365 days; return days, reason, and flag_type."""
    for i in range(1, 366):
        future = now + timedelta(days=i)
        flag_type, reason = get_flag_status(future)
        if flag_type != "no_flag":
            return i, reason, flag_type
    return -1, "Unknown", "no_flag"
