class ChuckNorris:

    async def main(self, bot, database, message, arguments):

        json_data = await bot.utils.web.get_content("http://api.icndb.com/jokes/random")

        chuck = bot.utils.json2obj(json_data)

        letter = ":cowboy: **| {}**".format(chuck.value.joke)

        await bot.say(message.channel, letter)
