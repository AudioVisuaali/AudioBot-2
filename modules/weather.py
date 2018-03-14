from random import randint
from datetime import datetime
from math import ceil as mceil
from urllib.request import quote

class Weather:

    async def main(self, bot, database, message, arguments):

        url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(quote(arguments[0]), bot.config.openweather.key)

        json_data = await bot.utils.web.get_content(url)

        weather = bot.utils.json2obj(json_data)

        try:
            definition = """Weather in: {}, {}```
Currently:    {}
Wind speed:   {} m/s
Current Temp: {} °C / {} °F
Max Temp:     {} °C / {} °F
Min Temp:     {} °C / {} °F
Sunrise:      {}
Sunset:       {}
Humidity:     {} %
Pressure:     {}00 Pa
Lon:          {}°
Lat:          {}```""".format(
                weather.name,
                weather.sys.country,
                weather.weather[0].description,
                weather.wind.speed,
                mceil((weather.main.temp-273.15)*10)/10,
                mceil(((weather.main.temp-273.15)*9/5+32)*10)/10,
                mceil((weather.main.temp_max-273.15)*10)/10,
                mceil(((weather.main.temp_max-273.15)*9/5+32)*10)/10,
                mceil((weather.main.temp_min-273.15)*10)/10,
                mceil(((weather.main.temp_min-273.15)*9/5+32)*10)/10,
                datetime.fromtimestamp(weather.sys.sunrise).strftime('%Y-%m-%d %H:%M:%S')[11:16],
                datetime.fromtimestamp(weather.sys.sunset).strftime('%Y-%m-%d %H:%M:%S')[11:16],
                weather.main.humidity, weather.main.pressure, weather.coord.lon, weather.coord.lat)

        except KeyError:
            definition = "No match was found"

        letter = ":earth_africa: **| {}**".format(definition)

        await bot.say(message.channel, letter)
