from random import randint
from json import load
import asyncio

class Joke:

    async def get_joke(self, jokes):

        for _ in range(20):
            joke = jokes[randint(0,len(jokes)-1)]
            if len(joke["title"]) + len(joke["body"]) < 200:
                return joke

    async def main(self, bot, database, message, arguments):

        data = load(open('./maps/joke_list.json'))

        joke = await self.get_joke(data)

        letter = ":joy: **| {}**\n`{}`".format(joke["title"], joke["body"])

        await bot.say(message.channel, letter)
