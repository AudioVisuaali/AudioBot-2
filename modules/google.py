from urllib.request import quote
from json import loads

class Google:

    async def main(self, bot, database, message, arguments):

        url = "https://www.googleapis.com/customsearch/v1?key={}&cx=008050020608944106700:shzflckcpo4&q={}".format(bot.config.google.key, quote(arguments[0]))
        json_data = await bot.utils.web.get_content(url)
        page = loads(json_data)

        letter = ":mag_right: **| Here's your result for: **__{}__\n\n:one: **{}**\n<{}>\n\n:two: **{}**\n<{}>\n\n:three: **{}**\n<{}>\n".format(arguments[0], page["items"][0]["title"], page["items"][0]["link"], page["items"][1]["title"], page["items"][1]["link"], page["items"][3]["title"], page["items"][3]["link"])

        await bot.say(message.channel, letter)
