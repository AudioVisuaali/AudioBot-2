from math import floor as mfloor

class Transfer:

    # Waiting for confirmation
    def guess_check(self, m):
        if m.content == "PENIS":
            return True
        else:
            return False

    async def main(self, bot, database, message, arguments):

        user = bot.database.user.get(message.author.id).points

        #!? give all points
        if arguments[1] == "all":
            arguments[1] == user

        try:
            amount = int(arguments[1])
        except ValueError:
            await bot.say(message.channel, "Invalid amount")
            return

        if user < amount:
            await bot.say(message.channel, "You don't have enough memes!")
            return

        # less than 10
        if amount < 10:
            await bot.say(message.channel, "transfer at least 10 memes!")
            return

        # Transferring to user instance
        user_getting = await bot.utils.get_user_instance(message.server, arguments[0])
        if user_getting is None:
            await bot.say(message.channel, "can't find user")
            return

        # checking if sending money toself
        if user_getting == message.author:
            await bot.say(message.channel, "Can't send money to yourself!")
            return

        letter = ":no_entry:** Olet siirtämässä __{}__ meemiä käyttäjälle {}!**\n\nTAX: **{}:money_with_wings: - 20% => {}:money_with_wings:**\nSinun meemisi: **{}:money_with_wings: -> {}:money_with_wings:**\n\n **Hyväksy** seuraavan 20 sekunnin aikana **kirjoittamalla: __PENIS__**".format(amount, user_getting.name, amount, mfloor(int(amount) * 80 / 100), user, str(int(user)-int(amount)))
        keepo = await bot.say(message.channel, letter)

        # Waiting for right response from user
        guess = await bot.wait_for_message(timeout=20.0, author=message.author, check=self.guess_check)

        # After time passes
        if guess is None:
            letter = ":no_entry_sign: **| Transaction cancelled!**"
            await bot.edit_message(keepo, letter)

        # After confirmed
        elif guess.content == "PENIS":
            # adding and removing points SOME NASTY MATH
            bot.database.user.points_alter(message.author.id, -amount)
            bot.database.user.points_alter(user_getting.id, amount)
            bot.database.server.tax_pot_alter(message.server.id, int(mfloor(int(amount) * 20 / 100)))

            # Sending message
            await bot.delete_message(keepo)
            await bot.say(message.channel, ":white_check_mark: **| Siirto onnistui!**")
            bot.database.pointhistory.add(message.author.id, message.server.id, 7, "Transfer", False, amount, "", "-"+str(amount), "", user_getting.name, "", "", "", 0, 0, int(amount))
            bot.database.pointhistory.add(user_getting.id, message.server.id, 7, "Transfer", False, "", "", "+"+str(amount), "", message.author.name, "", "", "", 0, int(amount), 0)
