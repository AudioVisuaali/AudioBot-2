class Ping:

    async def main(self, bot, database, message, arguments):

        # Get name
        name = bot.utils.author_nickanme(message.author)

        # Send message
        await bot.say(message.channel, "**:poop: | {} Pong!**".format(name))
