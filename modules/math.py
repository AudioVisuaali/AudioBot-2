from random import randint
import asyncio
from utils import nps
from math import ceil
from utils.web import Web

class Math:

    async def main(self, bot, database, message, arguments):

            name = bot.utils.author_nickanme(message.author)

            # Calling function
            nsp = nps.NumericStringParser()
            try:
                result = nsp.eval(arguments[0])
            except ZeroDivisionError:
                result = "an error, can't divide with zero!"

            # removing .0 when value is int
            try:
                b = ceil(result)
                if result == b:
                    result = b
            except:
                pass

            # Checking for 69
            if result == 69 or result == 69.69:
                eggplant = ":eggplant:"
            else:
                eggplant = ""

            # Creating message
            letter = ":cancer: **| {} it's {} {}**".format(name, str(result), eggplant)
            await bot.say(message.channel, letter)
