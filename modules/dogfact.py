from random import randint

class DogFact:

    async def main(self, bot, database, message, arguments):

        json_data = await bot.utils.web.get_content("http://dog-api.kinduff.com/api/facts")

        dog = bot.utils.json2obj(json_data)

        emoji = [":dog:", ":dog2:"][randint(0,1)]

        letter = "{} **| {}**".format(emoji, dog.facts[0])

        await bot.say(message.channel, letter)
