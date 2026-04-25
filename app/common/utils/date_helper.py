

import logging
from datetime import datetime,time, timedelta, timezone

import pytz

IST = pytz.timezone("Asia/Kolkata")

def get_utc_datetime():
    return datetime.now(timezone.utc)


def get_ist_datetime():
    return datetime.now(timezone.utc).astimezone(IST)

def get_ist_naive():
    return datetime.now(timezone.utc).astimezone(IST).replace(tzinfo=None)

# def ensure_ist(dt):
#     if dt is None:
#         return None
#     if dt.tzinfo is None:
#         return dt.replace(tzinfo=IST)
#     return dt.astimezone(IST)

def ensure_ist(dt):
    if dt is None:
        return None

    # DB gives naive IST → attach timezone properly
    return IST.localize(dt)

class ISTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ist = pytz.timezone("Asia/Kolkata")
        dt = datetime.fromtimestamp(record.created, ist)
        return dt.strftime(datefmt or "%Y-%m-%d %H:%M:%S")

def to_timedelta(value):
    if isinstance(value, timedelta):
        return value
    h, m, s = map(int, value.split(":"))
    return timedelta(hours=h, minutes=m, seconds=s)

def timedelta_to_time(value):
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
    else:
        parts = value.split(":")

        if len(parts) == 2:
            h, m = map(int, parts)
            s = 0
        elif len(parts) == 3:
            h, m, s = map(int, parts)
        else:
            raise ValueError("Invalid time format. Expected HH:MM or HH:MM:SS")

        total_seconds = h * 3600 + m * 60 + s

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return time(hours, minutes, seconds)

def make_utc(dt):
    if dt is None:
        return None

    # MySQL returned naive datetime, but it IS UTC
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc)