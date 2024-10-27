import datetime
import os
import re
import time
from functools import wraps

epoch = datetime.datetime.utcfromtimestamp(0)


def time_millis():
    return int(time.time() * 1000)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def handle_db_session(db_session):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            finally:
                db_session.remove()
        return wrapper
    return decorator


def clean_string(input_string: str) -> str:
    input_string = input_string.replace('\n', ' ')
    cleaned_string = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚ\s]', '', input_string)
    return cleaned_string
