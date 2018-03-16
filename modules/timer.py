from asyncio import sleep as asleep

class Timer:

    async def main(self, bot, database, message, arguments):

        try:
            time = arguments[0]
            time_to_sleep = int(time)
        except:
            await bot.say(message.channel, ":x: **| Invalid input**")
            return

        letter = ":clock1: **| <@{}> Notifying you in {} seconds!**".format(message.author.id, time)
        delete = await bot.say(message.channel, letter)

        await asleep(time_to_sleep)
        await bot.delete_message(delete)

        letter = ":clock1: **| <@{}> Time's up!**".format(message.author.id)
        await bot.say(message.channel, letter)
