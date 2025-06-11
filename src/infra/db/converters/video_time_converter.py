from datetime import date, datetime, time
from typing import Optional


def time_to_seconds(t: Optional[time]) -> Optional[int]:
    if t is None:
        return None
    return t.hour * 3600 + t.minute * 60 + t.second


def date_to_datetime_start(d: Optional[date]) -> Optional[datetime]:
    if d is None:
        return None
    return datetime.combine(d, time.min)

def date_to_datetime_end(d: Optional[date]) -> Optional[datetime]:
    if d is None:
        return None
    return datetime.combine(d, time.max)
