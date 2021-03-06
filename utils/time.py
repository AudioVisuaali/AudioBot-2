import aiohttp
import asyncio
from datetime import datetime, timedelta

class Time:

    def seconds_so_far_today(self):

        now = datetime.today()
        time_start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        delta = now - time_start_of_today

        return delta.seconds

    def time_untill_weekly(self, day, seconds):
        """time untill certain point in a day repeates weekly"""
        now = datetime.today()

        # Weekday in number foramt
        total_seconds_this_week_so_far = (now.weekday())*86400 + self.seconds_so_far_today()

        # current time ahead
        if ((day * 86400) + seconds) < total_seconds_this_week_so_far:
            return 604800 - (total_seconds_this_week_so_far - (day*86400 + seconds))

        # current time behind now behind
        else:
            return ((day * 86400) + seconds) - total_seconds_this_week_so_far

    def day_splitted_by_time(self, in_seconds):
            # how many days until epoch
            epoch = datetime.utcfromtimestamp(0)
            now = datetime.today()
            d = now - epoch

            # time until X time in day
            time_start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
            time_diff = now - time_start_of_today

            # Removing day if not reached time yet
            if time_diff.seconds > in_seconds:
                return d.days
            else:
                return d.days - 1
