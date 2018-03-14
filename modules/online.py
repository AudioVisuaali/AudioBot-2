import asyncio
from datetime import datetime

class BotStart:

    def create(self, d):

        class Rdeg:
            def __init__(self, d):
                self.days = "{}d ".format(d.day-1)
                self.hours = "{}h ".format(d.hour)
                self.minutes = "{}m ".format(d.minute)
                self.seconds = "{}s".format(d.second)

        return Rdeg(d)

    async def time_diff(self, start_up):

        time_now = datetime.now()
        delta = time_now - start_up
        seconds = delta.total_seconds()
        return delta

    async def format_time(self, delta):

        d = datetime(1,1,1) + delta

        formatted = self.create(d)

        if d.day-1 == 0:
            formatted.days = ""
            if d.hour == 0:
                formatted.hours = ""
                if d.minute == 0:
                    formatted.minutes = ""
                    if d.second == 0:
                        formatted.seconds = ""

        letter = "{}{}{}{}".format(formatted.days, formatted.hours, formatted.minutes, formatted.seconds)

        return letter

    async def main(self, bot, database, message, arguments):

        start = bot.utils.starttime
        seconds = await self.time_diff(start)
        started = await self.format_time(seconds)

        restarts = database.cache.botinfo.total_restarts

        letter = ":clock10: **| Bot has been online for {} and has been restarted {} times!**".format(started, restarts)

        await bot.say(message.channel, letter)
