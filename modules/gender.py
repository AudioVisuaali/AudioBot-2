from math import ceil as mceil
from urllib.request import quote

class Gender:

    async def main(self, bot, database, message, arguments):

        name = arguments[0]

        url = "https://api.genderize.io/?name=".format(quote(arguments[0]))

        json_data = await bot.utils.web.get_content(url)

        gender = bot.utils.json2obj(json_data)

        if gender is None:
            letter = "Module not working :thinking:"
        elif gender.gender == None:
            letter = "No data was found for {}!".format(name)
        else:
            letter = "There's a {}% of {} being a {}!".format(mceil(gender.probability * 100), name, gender.gender)

        letter = ":alien: **| {}**".format(letter)

        await bot.say(message.channel, letter)
