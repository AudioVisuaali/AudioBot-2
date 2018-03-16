from asyncio import sleep as asleep
from random import randint

class Duel:

    # Waiting for confirmation
    def guess_check(self, m):

        if str(message.author.id) in m.content:

            return True
        else:
            return False

    async def main(self, bot, database, message, arguments):

        owner = message.author
        slave = await bot.utils.get_user_instance(message.server, arguments[0])

        owner_name = bot.utils.author_nickanme(owner)
        slave_name = bot.utils.author_nickanme(slave)

        duel_amount = arguments[1]

        # Checking currency
        if not duel_amount.isdigit():
            no_currency = "**:crossed_swords: | {}, invalid amount of currency!**".format(owner_name)
            await bot.say(message.channel, no_currency)
            return

        # Checking if dueling self
        if owner.id == slave.id:
            await bot.say(message.channel, "**:crossed_swords: | {}, you can't duel yourself!**".format(owner_name))
            return

        # Checking if duleing bots
        if slave.bot:
            no_bot_duel = "**:crossed_swords: | {} you can't duel bots!**".format(owner_name)
            await bot.say(message.channel, no_bot_duel)
            return

        # Getting stats
        owner_points = bot.database.user.get(owner.id).points
        slave_points = bot.database.user.get(slave.id).points

        # Users do not have enough points to gamble
        if (int(duel_amount) > int(owner_points)) or (int(duel_amount) > int(slave_points)):
            more_points = "**:crossed_swords: | {} get some more points! :thinking:**".format(slave_name)
            await bot.say(message.channel, more_points)
            return

        # Checking if dueling with less than 10 currency
        if int(duel_amount) < 10:
            no_memes = "**:crossed_swords: | {} you have to duel atleast 10 memes!**".format(owner_name)
            await bot.say(message.channel, no_memes)
            return

        # Sending challenge message for dueller
        keepo = "<@{}> You have been **challenged** by **{}** for **{}** memes, you have **20** seconds to accept the duel by typing \n!accept <@{}> or !decline".format(slave.id, owner_name,duel_amount, owner.id)
        message_send = await bot.say(message.channel, keepo)

        # Waiting response form
        guess = await bot.wait_for_message(timeout=20.0, author=slave, check=self.guess_check)

        # Checking if challnged responded
        if guess is None:
            no_response = "**:crossed_swords: | {} did not response to the duel!**".format(slave_name)
            await bot.edit_message(message_send, no_response)
            return

        # Checking if challenged accepts
        else:
            if guess.content.startswith("!decline"):
                await bot.delete_message(kappa)
                await bot.say(message.channel, "**:crossed_swords: | {} declined to the duel!**".format(slave_name))
                return

            # Sending message for rolling and deleting a message for clearness
            await bot.delete_message(message_send)
            msg = await bot.say(message.channel, "<:reeee:312321001398730762> **Rolling**")
            await asleep(1.5)
            letter = ""

            #player 1 wins
            if randint(0, 99) < 50:
                # Message content
                letter = "**:crossed_swords: | {} won {} memes!**"''.format(owner_name, str(int(duel_amount)*2))
                bot.database.pointhistory.add(owner.id, message.server.id, 3, "Duel", False, duel_amount, "", "+"+duel_amount, "", slave_name, "", "", "", 0, int(duel_amount), 0)
                bot.database.pointhistory.add(slave.id, message.server.id, 3, "Duel", False, duel_amount, "", "-"+duel_amount, "", owner_name, "", "", "", 0, 0, int(duel_amount))

                # Adding/removing points
                bot.database.user.points_alter(owner.id, duel_amount)
                bot.database.user.points_alter(slave.id, duel_amount)

            # Player 2 wins
            else:
                # Message content
                letter = "**:crossed_swords: | {} won {} memes!**"''.format(slave_name, str(int(duel_amount)*2))
                bot.database.pointhistory.add(owner.id, message.server.id, 3, "Duel", False, duel_amount, "", "-"+duel_amount, "", slave_name, "", "", "", 0, 0, int(duel_amount))
                bot.database.pointhistory.add(slave.id, message.server.id, 3, "Duel", False, duel_amount, "", "+"+duel_amount, "", owner_name, "", "", "", 0, int(duel_amount), 0)
                # Adding/removing points
                bot.database.user.points_alter(owner.id, -duel_amount)
                bot.database.user.points_alter(slave.id, duel_amount)

            # Posting the result in chat
            await bot.edit_message(msg, letter)
