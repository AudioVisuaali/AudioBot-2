import asyncio

class RemoveCommand:

    async def main(self, bot, database, message, arguments):

        if not database.command.exists(message.server, arguments[0]):
            letter = ":ballot_box_with_check:  **| Command __{}__ doesn't exist in the database!**"


        else:
            database.command.remove(message.server, arguments[0])

            letter = ":white_check_mark: **| Command __{}__ removed database!**"

        await bot.say(message.channel, letter.format(arguments[0]))
