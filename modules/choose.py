import asyncio
from random import randint

class Choose:

    async def main(self, bot, database, message, arguments):

        if len(arguments) < 2: return

        pos = randint(0, len(arguments)-1)

        letter = "{} {}".format(message.author.mention, arguments[pos])

        await bot.say(message.channel, letter)
