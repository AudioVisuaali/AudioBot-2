from random import randint

class NumberFact:

    async def main(self, bot, database, message, arguments):

        # Random number if user didn't say anything
        if not arguments:
            number = str(randint(0,10000))
        else:
            number = arguments[0]

        # Fetch a numberfact
        query = "http://numbersapi.com/{}/trivia?notfound=floor&fragment".format(number)
        numberfact = await bot.utils.web.get_content(query)

        # Sending message
        letter = ":underage:  **| The number {} is {}**".format(number, numberfact)
        await bot.say(message.channel, letter)
