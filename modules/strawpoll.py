from strawpy import create_poll

class StrawPoll:

    async def main(self, bot, database, message, arguments):

        name = bot.utils.author_nickanme(message.author)

        # Popping question to it's own variation
        question = arguments.pop(0)
        print(question)
        print(arguments)
        # Creating poll
        kek = ["yes", "no","asd"]
        #new_poll = create_poll(question, arguments)
        new_poll = create_poll("question", ["yes", "no","asd"])
        # Sending message
        letter = "**Here's your poll, {}**\n{}".format(name, new_poll.url)
        await bot.say(message.channel, letter)
