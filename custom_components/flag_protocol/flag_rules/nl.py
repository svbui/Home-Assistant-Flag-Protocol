from datetime import datetime, timedelta

def get_flag_status(now: datetime) -> tuple[str, str]:
    days = [
        ((1, 31), lambda d: d.weekday() != 6, "full_mast_with_banner", "Princess Beatrix’s Birthday"),
        ((2, 1), lambda d: d.weekday() == 0, "full_mast_with_banner", "Princess Beatrix’s Birthday (Monday)"),
        ((4, 26), lambda d: d.weekday() == 5, "full_mast_with_banner", "King’s Day (Saturday)"),
        ((4, 27), lambda d: d.weekday() != 6, "full_mast_with_banner", "King’s Day"),
        ((5, 4), None, "half_mast", "Remembrance Day"),
        ((5, 5), None, "full_mast", "Liberation Day"),
        ((5, 17), lambda d: d.weekday() != 6, "full_mast_with_banner", "Queen Maxima’s Birthday"),
        ((5, 18), lambda d: d.weekday() == 0, "full_mast_with_banner", "Queen Maxima’s Birthday (Monday)"),
        ((6, None), lambda d: d.weekday() == 5 and (d + timedelta(days=7)).month != 6, "full_mast", "Veterans Day"),
        ((8, 15), lambda d: d.weekday() != 6, "full_mast", "End of WWII"),
        ((8, 16), lambda d: d.weekday() == 0, "full_mast", "WWII Commemoration (Monday)"),
        ((9, None), lambda d: d.weekday() == 1 and 15 <= d.day <= 21, "full_mast", "Prinsjesdag"), 
        ((12, 7), lambda d: d.weekday() != 6, "full_mast_with_banner", "Princess of Orange’s Birthday"),
        ((12, 8), lambda d: d.weekday() == 0, "full_mast_with_banner", "Princess of Orange’s Birthday (Monday)"),
        ((12, 15), lambda d: d.weekday() != 6, "full_mast", "Kingdom Day"),
        ((12, 16), lambda d: d.weekday() == 0, "full_mast", "Kingdom Day (Monday)")
    ]
    for (month, day), condition, flag_type, reason in days:
        if (day is None and now.month == month and condition and condition(now)) or (now.month == month and now.day == day and (not condition or condition(now))):
            return flag_type, reason
    return "no_flag", "No flag today"

def get_next_flag_day(now: datetime) -> tuple[int, str, str]:
    for i in range(1, 366):
        future = now + timedelta(days=i)
        flag_type, reason = get_flag_status(future)
        if flag_type != "no_flag":
            return i, reason, flag_type
    return -1, "Unknown", "no_flag"
