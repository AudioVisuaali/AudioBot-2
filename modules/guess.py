from random import randint

class Guess:

    def guess_check(self, m):
        return m.content.isdigit()

    async def main(self, bot, database, message, arguments):

        await bot.say(message.channel, '**Guess a number between 1 to 10**')

        guess = await bot.wait_for_message(timeout=5.0, author=message.author, check=self.guess_check)
        answer = randint(1, 10)

        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await bot.say(message.channel, fmt.format(answer))
            return

        if int(guess.content) == answer:
            await bot.say(message.channel, '**You are right!**')
        else:
            await bot.say(message.channel, '**Sorry. It is actually {}.**'.format(answer))
