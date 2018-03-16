class SetAvatar:

    async def main(self, bot, database, message, arguments):

        if message.attachments:
            url = message.attachments[0]["url"]
        elif arguments:
            url = arguments[0]
        else:
            await bot.say(message.channel, ":wrench: **| Give a file or a link**")

        try:
            res = await bot.utils.web.get_image(url, bot)
            await bot.say(message.channel, ":wrench: **| Avatar changed**")
        except Exception as e:
            if "400" in e:
                e = e + "if 400 try again later, too many requests"
            await bot.say(message.channel, ":wrench: **| ERROR:** `{}`".format(e))
