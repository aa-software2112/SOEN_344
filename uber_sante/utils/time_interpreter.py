import datetime
import time

class TimeInterpreter:

    SECONDS_IN_HOUR = 60*60
    SECONDS_IN_MINUTE = 60

    def get_start_time_string(self, start):
        return "{}:{}0 {}".format(int(start / (TimeInterpreter.SECONDS_IN_HOUR)),
                                 int((start % TimeInterpreter.SECONDS_IN_HOUR) / TimeInterpreter.SECONDS_IN_MINUTE),
                                 "AM" if start / (TimeInterpreter.SECONDS_IN_HOUR) < 12 else "PM")
    def get_time_to_second(self, value):
        x = time.strptime(value.split(',')[0], '%H:%M')

        return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
