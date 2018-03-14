from utils.time import Time
from math import ceil as mceil

import asyncio
from random import randint
class Bank:

    async def main(self, bot, database, message, arguments):

        interest = 5

        # wealth
        userRR = bot.database.user.get(message.author.id)
        users_points = userRR.points
        users_bank = userRR.bank
        add_dir = ["add", "deposit", "put", "give"]
        take_dir = ["take", "withdraw", "remove"]

        # How many memes in bank
        if len(arguments) == 0:

            # Time from interest
            BANK_INTEREST_DAY = 3
            BANK_INTEREST_TIME = 3000
            time = Time()
            past_time = 604800 - (time.time_untill_weekly(BANK_INTEREST_DAY, BANK_INTEREST_TIME))

            # Users interest
            try:
                users_own_interest = mceil((bot.database.pointhistory.get_min_bank_amount(10, past_time, message.author.id)[0].min_bank) * interest / 100)
            except:
                users_own_interest = mceil(users_bank * interest / 100)


            # Creating message and sending it
            letter = ":bank: **| You have {} memes in your bank! Interest is {}%, Currently: {} memes\n\nInterest is calculated by the amount of memes you've had in the bank for the past week!\nYou receive interest every wednesday @ 00:00 **".format(users_bank, interest, users_own_interest)
            await bot.say(message.channel, letter)
            return

        # if all
        if arguments[1] in ["all", "kaikki"]:

            # Check if add or take
            if arguments[0] in add_dir:
                amount = users_points
            elif arguments[0] in take_dir:
                amount = users_bank

        elif arguments[1] in ["half", "puolet","1/2"]:

            # Check if add or take
            if arguments[0] in add_dir:
                amount = mceil(users_points * 0.5)
            elif arguments[0] in take_dir:
                amount = mceil(users_bank * 0.5)

        elif arguments[1] in ["third","kolmasosa","1/3"]:

            # Check if add or take
            if arguments[0] in add_dir:
                amount = mceil(users_points * 0.33333)
            elif arguments[0] in take_dir:
                amount = mceil(users_bank * 0.33333)

        elif arguments[1] in ["quarter","quad","neljännes", "1/4"]:

            # Check if add or take
            if arguments[0] in add_dir:
                amount = mceil(users_points * 0.25)
            elif arguments[0] in take_dir:
                amount = mceil(users_bank * 0.25)

        # if not all try to set amount
        else:
            try:
                arguments[1] = arguments[1].replace("k", "000")
                amount = int(arguments[1])
            except:
                await bot.say(message.channel, ":bank: **| Invalid amount!**")
                return

        # Must use atleast 10 memes
        if amount < 10:
            await bot.say(message.channel, ":bank: **| You need to atleast use 10 memes!**")
            return


        # Adding memes
        if arguments[0] in add_dir:

            # Checking if usr has memes
            if amount > int(users_points):
                await bot.say(message.channel, ":bank: **| You don't have enough memes!**")
                return

            # calculating min amount in bank
            minimum = users_bank

            # Add to history
            bot.database.pointhistory.add(message.server.id, message.author.id, 10, "Bank", False, amount, "", "-"+str(amount), "", "To bank", "", "", "", minimum, 0, amount)

            # Set stats
            bot.database.user.points_alter(message.author.id, -amount)
            bot.database.user.bank_alter(message.author.id, amount)

            # letter
            await bot.say(message.channel, ":bank: **| You have transferred {} memes to bank!\n\nYou now have:\n:purse:: {} memes\n:bank:: {} memes**".format(amount, users_points - amount, users_bank + amount))
            return

        # Taking memes
        elif arguments[0] in take_dir:

            # Checking if enough memes in bank
            if amount > int(users_bank):
                await bot.say(message.channel, ":bank: **| You don't have that many memes in bank!**")
                return

            # calculating min amount in bank
            minimum = users_bank - amount

            # Add to history
            bot.database.pointhistory.add(message.server.id, message.author.id, 10, "Bank", False, amount, "", "+"+str(amount), "", "From bank", "", "", "", minimum, amount, 0)

            # Set stats

            bot.database.user.points_alter(message.author.id, amount)
            bot.database.user.bank_alter(message.author.id, -amount)

            # letter
            await bot.say(message.channel, ":bank: **| You have transferred {} memes to your wallet!\n\nYou now have:\n:purse:: {} memes\n:bank:: {} memes**".format(amount, users_points + amount, users_bank - amount))
            return
