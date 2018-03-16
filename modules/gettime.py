from urllib.request import quote
from math import floor as mfloor
from datetime import datetime
from time import time

class GetTime:

    async def main(self, bot, database, message, arguments):

        if not arguments:
            letter = ":clock11: **| Servers time is {}**".format(str(datetime.fromtimestamp(mfloor(time())).strftime('%H:%M')))
            await bot.say(message.channel, letter)

        else:
            google = quote(str(arguments[0]))
            query = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}&language={}".format(google, bot.config.google.key, "en")

            json_data = await bot.utils.web.get_content(query)
            geo = bot.utils.json2obj(json_data)

            if geo.status == "OK":
                lat = str(float("{0:.4f}".format(geo.results[0].geometry.location.lat)))
                lng = str(float("{0:.4f}".format(geo.results[0].geometry.location.lng)))

                query = "https://maps.googleapis.com/maps/api/timezone/json?location=%s,%s&timestamp=%s&key=%s&language=%s" % (lat, lng, time(), bot.config.google.key, "en")
                json_data = await bot.utils.web.get_content(query)
                location = bot.utils.json2obj(json_data)

                time_now = str(int(time() + location.rawOffset + location.dstOffset))
                time_in_hour_format = datetime.fromtimestamp(int(time_now)).strftime('%H:%M')
                time_in_weekday = datetime.fromtimestamp(int(time_now)).weekday()

                if   time_in_weekday == 0: day_is = "Monday"
                elif time_in_weekday == 1: day_is = "Tuesday"
                elif time_in_weekday == 2: day_is = "Wednesday"
                elif time_in_weekday == 3: day_is = "Thursday"
                elif time_in_weekday == 4: day_is = "Friday"
                elif time_in_weekday == 5: day_is = "Saturday"
                elif time_in_weekday == 6: day_is = "Sunday"

                letter = ":clock11: **| Time in {} is {} and the day is {}**".format(geo.results[0].formatted_address, time_in_hour_format, day_is)
                await bot.say(message.channel, letter)
