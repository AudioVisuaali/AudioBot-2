import asyncio

class AddCommand:

    async def main(self, bot, database, message, arguments):

        if database.command.exists(message.server, arguments[0]):
            letter = ":x: **| Command __{}__ already exists in the database!**"

        else:
            command = database.command.add(message.server, message.author,
                                            arguments[0], arguments[1])

            letter = ":white_check_mark: **| Command __{}__ added to the database!**"

        await bot.say(message.channel, letter.format(arguments[0]))
