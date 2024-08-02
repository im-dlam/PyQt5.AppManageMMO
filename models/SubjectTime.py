import time as tg
import random
from datetime import datetime

def time():
    tg.sleep(1)

def time_rand():
    tg.sleep(float(random.randrange(1,10)/35))

def time_lastest(time_str):
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    datetime_object = datetime.now() - datetime.strptime(time_str, time_format)
    if datetime_object.seconds < 3600 and datetime_object.days == 0:
        if datetime_object.seconds < 60:
            return f"{datetime_object.seconds} seconds ago"
        else:
            return f"{int(datetime_object.seconds /  60)} minutes ago"
    elif datetime_object.seconds >= 3600 and datetime_object.seconds < 86400 and datetime_object.days == 0:
        return f"{int(datetime_object.seconds /  3600)} hours ago"
    else:
        return f"{datetime_object.days} days ago"
