class UserPoints:

    async def main(self, bot, database, message, arguments):
        # TODO ADD ANOTHER USERS POINTS CHECK
        letter = ""

        author = message.author

        name = bot.utils.author_nickanme(author)

        user = bot.database.user.get(author.id)

        letter = "**:money_with_wings:  | {} you have {} ({}+{}) memes!** ".format(name, user.points + user.bank, user.points, user.bank)

        await bot.say(message.channel, letter)
