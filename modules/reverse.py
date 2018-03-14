class Reverse:

    async def main(self, bot, database, message, arguments):

        #this reverses it LOL
        await bot.say(message.channel, "**:arrows_counterclockwise: {}**".format(arguments[0][::-1]))
