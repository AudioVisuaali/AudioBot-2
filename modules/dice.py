import asyncio
from random import randint

class Dice:

    async def main(self, bot, database, message, arguments):

        try:
            high = int(arguments[0])
        except:
            high = 6

        letter = ":game_die: **| Dice rolled {}**".format(randint(1, high))

        await bot.say(message.channel, letter)
