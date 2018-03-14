class CatFact:

    async def main(self, bot, database, message, arguments):

        json_data = await bot.utils.web.get_content("https://catfact.ninja/fact")

        cat = bot.utils.json2obj(json_data)

        letter = ":cat: **| {}**".format(cat.fact)

        await bot.say(message.channel, letter)
