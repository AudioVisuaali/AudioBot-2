class Tokens:

    async def main(self, bot, database, message, arguments):

        if arguments:
            user = await bot.utils.get_user_instance(arguments[0])
            if user is None:
                return

        else:
            user = message.author

        tokens = bot.database.user.get(user.id).tokens
        name = bot.utils.author_nickanme(user)

        letter = ":trophy: **| {} has {} tokens!**".format(name, tokens)
        await bot.say(message.channel, letter)
