class Gamble:

    async def main(self, bot, database, message, arguments):

        # stuff
        rows, state1, state2, state3, limit, owner = [], 6, 7, 9, 20, message.author
        letter = ":closed_book: **| This is your gambling history!**\n"

        # nothing special
        if len(arguments) == 0:
            pass

        # amnount or different user
        elif len(arguments) == 1:
            try:
                if int(arguments[0]) <= 40:
                    limit = int(arguments[0])
                else:
                    limit = 40

            except:
                owner = await bot.utils.get_user_instance(message.server, arguments[0])
                if owner is None:
                    return

                name = bot.utils.author_nickanme(owner)
                letter = ":closed_book: **| This is {}'s gambling history!**\n".format(name)


        # different user and amount
        elif len(arguments) == 2:
            try:
                if int(arguments[1]) <= 40:
                    limit = int(arguments[1])
                else:
                    limit = 40

                owner = await bot.utils.get_user_instance(message.server, arguments[0])
                if owner is None:
                    return

                name = bot.utils.author_nickanme(owner)
                letter = ":closed_book: **| This is {}'s gambling history!**\n".format(name)

            except:
                return

        # Get stats
        #get = points_stats_get_without_server(owner.id, limit)
        #(self, user, d_id, total = 10):
        get = bot.database.pointhistory.get_history_user(owner.id, limit)
#SELECT server_id, mode_id, mode, stake1, stake2, outcome1, outcome2, info1, info2, info3, info4_hidden, first_contact FROM

        for row in get:

            # Cimplified :) and Name
            temporary, temp1, temp2, temp3 = [], [], [], []
            temporary.append(row.mode_name)

            # stakes
            if not row.stake_points == "":
                temp1.append(row.stake_points + "m")
            if not row.stake_tokens == "":
                temp1.append(row.stake_tokens + "t")
            temporary.append(", ".join(temp1))

            #outcome
            if not row.outcome_points == "":
                temp2.append(row.outcome_points + "m")
            if not row.outcome_tokens == "":
                temp2.append(row.outcome_tokens + "t")
            temporary.append(", ".join(temp2))

            #info
            if not row.info1 == "":
                temp3.append(row.info1.replace(":",""))
            if not row.info2 == "":
                temp3.append(row.info2.replace(":",""))
            if not row.info3 == "":
                temp3.append(row.info3.replace(":",""))
            temporary.append(", ".join(temp3))
            rows.append(temporary)

        # Checking largest rows for each section in "exel"
        for row in rows:
            if len(row[0]) > state1:
                state1 = len(str(row[0]))
            if len(row[1]) > state2:
                state2 = len(str(row[1]))
            if len(row[2]) > state3:
                state3 = len(str(row[2]))

        # I like this is simple when you get it
        letter += "```py\nName  {}| Stake  {}| Outcome  {}| Info\n".format(" "*(state1 - 4), " "*(state2 - 5), " "*(state3 - 7))

        # Creating actual table
        for row in rows:
            letter += "{}{}    {}{}    {}{}    {}\n".format(row[0], " "*(state1-len(str(row[0]))), row[1], " "*(state2-len(str(row[1]))), row[2], " "*(state3-len(str(row[2]))), row[3])
        letter += "```\n**Result in order of time,  __m = memes__  and  __t = tokens__\n\nMore options coming in the future for biggest bets etc!**"

        # send
        await bot.say(message.channel, letter)
