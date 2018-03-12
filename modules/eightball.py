import asyncio
from random import randint
class EightBall:

    async def main(self, bot, database, message, arguments):

        if len(arguments[0]) < 7:
            return

        eightball = bot.utils.eightBall

        item = randint(0, len(eightball)-1)

        await bot.say(message.channel, eightball[item])
