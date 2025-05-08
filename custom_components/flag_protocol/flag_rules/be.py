from datetime import datetime, timedelta

def get_flag_status(now: datetime) -> tuple[str, str]:
    fixed = [
        (1, 20, "full_mast", "Queen Mathilde’s Birthday"),
        (2, 17, "full_mast", "Royal Family Memorial"),
        (4, 7,  "full_mast", "Tribute to Fallen Peacekeepers"),
        (4, 15, "full_mast", "King Philippe’s Birthday"),
        (5, 1,  "full_mast", "Labour Day"),
        (5, 5,  "full_mast", "Council of Europe Day"),
        (5, 8,  "full_mast", "Victory in Europe Day"),
        (5, 9,  "full_mast", "Europe Day"),
        (6, 6,  "full_mast", "King Albert II’s Birthday"),
        (7, 2,  "full_mast", "Royal Wedding Anniversary"),
        # National Day: 21,22,23 July
        (7, 21, "full_mast", "National Day"),
        (7, 22, "full_mast", "National Day"),
        (7, 23, "full_mast", "National Day"),
        (9, 11, "full_mast", "Queen Paola’s Birthday"),
        (10,24, "full_mast", "United Nations Day"),
        (11,11, "half_mast","Armistice Day"),
        (11,15, "full_mast","King’s Feast"),
        (12,4,  "full_mast", "Royal Wedding Anniversary")
    ]
    for month, day, flag_type, reason in fixed:
        if now.month == month and now.day == day:
            return flag_type, reason
    return "no_flag", "No flag today"

def get_next_flag_day(now: datetime) -> tuple[int, str, str]:
    for i in range(1, 366):
        future = now + timedelta(days=i)
        flag_type, reason = get_flag_status(future)
        if flag_type != "no_flag":
            return i, reason, flag_type
    return -1, "Unknown", "no_flag"
