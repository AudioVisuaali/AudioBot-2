class JoinedToServer:

    async def main(self, bot, database, message, arguments):

        if not arguments:
            owner = message.author
        else:
            owner = await bot.utils.get_user_instance(message.server, arguments[0])

        name = bot.utils.author_nickanme(owner)

        letter = "**:calendar_spiral: | {} joined the server on {}**".format(name, str(owner.joined_at)[:-7])

        await bot.say(message.channel, letter)
