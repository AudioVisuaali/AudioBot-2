from math import ceil as mceil
from urllib.request import quote

class GeoLocation:

    async def main(self, bot, database, message, arguments):

        url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}&language={}".format(quote(arguments[0]), bot.config.google.key, "en")

        json_data = await bot.utils.web.get_content(url)

        geo = bot.utils.json2obj(json_data)

        if geo.status == "OK":
            lat = "{0:.4f}".format(geo.results[0].geometry.location.lat)
            lng = "{0:.4f}".format(geo.results[0].geometry.location.lng)
            letter = ":earth_americas: **| {}\n__LAT:__ {}\n__LNG:__ {}**".format(geo.results[0].formatted_address, lat, lng)

        else:
            letter = "Google has some broplems with their servers or my servers connection is scuffed LUL"

        await bot.say(message.channel, letter)
