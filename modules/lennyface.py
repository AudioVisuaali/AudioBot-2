from random import randint
import asyncio

class Lennyface:

    async def main(self, bot, database, message, arguments):

        lennyface = bot.utils.lennyfaces

        item = randint(0, len(lennyface)-1)

        await bot.say(message.channel, lennyface[item])
