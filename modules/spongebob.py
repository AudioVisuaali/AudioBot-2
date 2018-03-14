class SpOnGeBoB:

    def spongebob_message(self, m):
        spongebobbed = ""
        i = True  # capitalize
        for char in m:
            if i:
                spongebobbed += char.upper()
            else:
                spongebobbed += char.lower()
            if char != ' ':
                i = not i
        return spongebobbed

    async def main(self, bot, database, message, arguments):

        splitted = list(arguments[0])

        letter = "**:arrows_clockwise: | {}**".format(self.spongebob_message(splitted))
        await bot.say(message.channel, letter)
