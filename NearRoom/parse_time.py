from datetime import datetime
from datetime import timedelta

def parse_start(time_string):
    time_string=str(time_string)
    try:
        if len(time_string) <= 2:
            time_format = '%H'
            parsed_time = datetime.strptime(time_string, time_format).time()
        else:
            time_format = '%H%M'
            parsed_time = datetime.strptime(time_string, time_format).time()
        return parsed_time
    except ValueError:
        raise ValueError('Invalid time format')


def parse_runtime(minutes):
    minutes = int(minutes)
    time_delta = timedelta(minutes=minutes)
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes = remainder // 60
    return "{:02d}:{:02d}".format(hours, minutes)
