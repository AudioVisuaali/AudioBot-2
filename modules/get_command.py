import asyncio

class GetCommand:

    async def main(self, bot, database, message, arguments):

        command = database.command.get(message.server, arguments)

        if command is None:
            return

        await bot.say(message.channel, command.response.format(message.author.mention))
