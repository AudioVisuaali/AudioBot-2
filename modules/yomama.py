class YoMama:

    async def main(self, bot, database, message, arguments):

        json_data = await bot.utils.web.get_content("http://api.yomomma.info/")

        mama = bot.utils.json2obj(json_data)

        letter = ":juggling: **| {}**".format(mama.joke)

        await bot.say(message.channel, letter)
