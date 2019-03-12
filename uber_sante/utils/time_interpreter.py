import datetime
import time

class TimeInterpreter:

    SECONDS_IN_HOUR = 60*60
    SECONDS_IN_MINUTE = 60

    def get_start_time_string(self, start):
        return "{}:{} {}".format(int(start / (self.SECONDS_IN_HOUR)),
                                 self.format_minutes(start),
                                 "AM" if start / (self.SECONDS_IN_HOUR) < 12 else "PM")
      
    def get_time_to_second(self, value):
        x = time.strptime(value.split(',')[0], '%H:%M')
        return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

    def add_20_minutes(self, value):
        return int(value) + 20 * self.SECONDS_IN_MINUTE

    def format_minutes(self, value):
        if value % TimeInterpreter.SECONDS_IN_HOUR == 0:
            return "00"
        else:
            return int((value % self.SECONDS_IN_HOUR) / self.SECONDS_IN_MINUTE)