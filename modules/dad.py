class Dad:

    async def main(self, bot, database, message, arguments):

        json_data = await bot.utils.web.get_content("https://icanhazdadjoke.com/slack")

        dad = bot.utils.json2obj(json_data)

        letter = ":older_man: **| {}**".format(dad.attachments[0].text)

        await bot.say(message.channel, letter)
