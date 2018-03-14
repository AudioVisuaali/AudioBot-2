from random import randint
from math import ceil as mceil
from asyncio import sleep as asleep

class Roulette:

    async def main(self, bot, database, message, arguments):

        # TODO make to botsettings special channels for serverspecific
            min_points = 10
            winrate = 50
            special_winrate = 50
            rand_low = 110
            rand_high = 140
            special_channels = ["404356322595962880"]
            multiplier_outcome_str = ""
            multiplier_outcome_multiplier_str = ""
            amount = arguments[0]
            name = bot.utils.author_nickanme(message.author)
            user_points = database.user.get(message.author.id).points

            #Validating input and roulette amount
            if amount != "all":

                # all in
                all_in = False

                # Checking for k=1000 points
                if "k" in amount:
                    try:
                        amount = float(arguments[0].lower().replace("k","")) * 1000
                    except ValueError:
                        return
                #Checking if number
                try:
                    user_gamble = int(amount)
                except ValueError:
                    return

            # Assigning users all points for !roulette all
            else:
                user_gamble = user_points
                all_in = True

            # Checking if user gambled mreo than x aoumnt of points
            if user_gamble < min_points:
                await bot.say(message.channel, "<@{}> **You have to gamble at least {} memes!**".format(message.author.id, min_points))
                return

            # Checking pointsif user_gamble > user_points
            if user_gamble > user_points:
                if user_gamble - user_points < 100:
                    need_points = user_gamble - user_points
                else:
                    need_points = "more"
                await bot.say(message.channel, "<@{}> **You don't have enough memes to gamble, you need {} memes!**".format(message.author.id, need_points))
                return

            # Cpecial channels
            if (message.channel.id in special_channels) and (randint(1,100) > special_winrate):

                # winrate
                winrate = special_winrate

                # Creating multiplier and some other stuff
                mvalue = float(randint(rand_low, rand_high) / 100)
                moutcome = int(mceil(user_gamble * mvalue - user_gamble))

                # str for message
                multiplier_outcome_str = "**+" + str(moutcome) + "**"
                multiplier_outcome_multiplier_str = "Multiplier " + str(mvalue)
                info3 = str(mvalue)

            # if not special
            else:
                info3 = ""
                moutcome = 0
                mvalue = 1

            # info for logging
            info1 = ""
            info2 = ""

            # Win
            if randint(1,100) < winrate:

                # Calculations for message formation later on
                outcome_total = user_gamble
                total_points = mceil(user_points + (outcome_total * mvalue))

                # Adding points and logging event for user
                user_gamble = user_gamble * mvalue
                database.user.points_alter(message.author.id, user_points)
                #users_set_points_to_plus(user_gamble, message.author.id)

                # Determine afterfix
                if all_in:
                    win_afterfix = ":confetti_ball: :confetti_ball:"
                    info2 = "All in"
                else:
                    win_afterfix = ":confetti_ball:"

                # Creating message
                letter = "** :slot_machine:  | {}, you have won {}{} memes, you now have {} memes! {} {}** ".format(name, outcome_total, multiplier_outcome_str, total_points, win_afterfix, multiplier_outcome_multiplier_str)
                try:
                    win_str_plus = "+" + str(int(outcome_total)+int(moutcome))
                    plus = int(outcome_total)+int(moutcome)
                except:
                    win_str_plus = "+" + str(int(outcome_total))
                    plus = int(outcome_total)

                minus = 0
                info1 = "Win"

            # Lose
            else:
                info3 = ""
                # Calculations for message formation later on
                outcome_total = user_gamble
                total_points = user_points - outcome_total


                #ddasd = user_gamble - (user_gamble * 2)
                database.user.points_alter(message.author.id, -user_gamble)

                # Determine afterfix
                if all_in:
                    win_afterfix = ":sob:"
                    info2 = "All in"
                else:
                    win_afterfix = ":cry:"


                # Creating message
                letter = "** :slot_machine:  | {}, you have lost {} memes, you now have {} memes! {}** ".format(name, outcome_total, total_points, win_afterfix)
                win_str_plus = "-" + str(user_gamble)
                plus = 0
                minus = int(user_gamble)
                info1 = "Lose"

            #points_stats_insert(message.server.id, message.author.id, 5, "Roulette", str(user_gamble), "", win_str_plus, "", info1, info2, info3, "", 0, plus, minus)

            # Sending message, checking if worth of excitement
            if user_gamble / user_points > 0.8:
                                                                    # TODO add expression system to config file
                msg = await bot.say(message.channel, "**:no_mouth: Rolling **")
                await asleep(4.0)
                await bot.edit_message(msg, letter)
                return

            # if not high bet do this no excitement
            else:
                await bot.say(message.channel, letter)
