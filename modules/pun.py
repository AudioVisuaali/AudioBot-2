class Pun:

    async def main(self, bot, database, message, arguments):

        json_data = await bot.utils.web.get_content("http://getpuns.herokuapp.com/api/random")

        pun = bot.utils.json2obj(json_data)

        await bot.say(message.channel, ":joy: **| {}**".format(pun.Pun))
