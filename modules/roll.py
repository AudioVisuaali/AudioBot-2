#import audiovisuaali
from random import randint
# from mysqlfiles import stats_roll_get_previous
# from mysqlfiles import stats_roll_add
# from mysqlfiles import points_stats_insert
#
# #roll (Rolls a random number between 0-100 if special arguments are not given)
# async def roll(message, client, arguments):
class Roll:

    async def main(self, bot, database, message, arguments):

        for i in arguments:
            try:
                int(i)
            except:
                return

        if len(arguments) == 0:
            first_slot = [0,1,2,3,4,5,6,7,8,9,""]
            second_slot =[0,1,2,3,4,5,6,7,8,9]
            first = str(first_slot[randint(0, 10)])
            second = str(second_slot[randint(0, 9)])
            if first == "0" and second in ["1","2","3","4","5","6","7","8","9"]:
                first = ""
            token, meme, double, memes, tokens = "", "", False, 0, 0

            # Checking if double
            if first == second:
                double = True

            # Getting roll history
            previous = await bot.timeout.check_roll(message.author.id)

            # Cheking if double, no history(for abuse)
            insert_meme = ""
            insert_token = ""
            info2 = ""
            win_asd = 0


            if first == second:
                info2 = "tuplat"

                if not previous:

                    # Add tokens
                    if randint(0,1000) == 342: # one in 10000
                        tokens = 1
                        bot.database.user.tokens_alter(tokens, message.author.id)
                        meme = " | You have won a token from roll!"
                        insert_token = "+"+str(tokens)
                        win_asd = 1


                    # Add memes
                    if randint(1,5) == 2:
                        memes = 10
                        bot.database.user.points_alter(memes, message.author.id)
                        token = " | You have won a {}memes from roll!".format(memes)
                        insert_meme = "+"+str(memes)
                        win_asd = 1

            # Add roll stats
            bot.database.double.add(message.author.id, first, second, double, memes, tokens)
            #stats_roll_add(message.author.id, first, second, double, memes, tokens)
            if win_asd == 1:
                bot.database.pointhistory.add(message.author.id, message.server.id, 1, "Roll", False, "", "", insert_meme, insert_token, first+second, info2, "", "", 0, 0, 0)

            # Formatting and sending message
            letter = "**{}{}{}{}**".format(first, second, token, meme)
            await bot.say(message.channel, "<@"+message.author.id+"> "+letter)
            await bot.timeout.add_roll(message.author.id)

        elif len(arguments) == 1:
            kek = randint(1, int(arguments[0]))
            await bot.say(message.channel, "<@"+message.author.id+"> "+str(kek))

        elif len(arguments)  == 2:
            kek = randint(int(arguments[0]), int(arguments[1]))
            await bot.say(message.channel, "<@"+message.author.id+"> "+str(kek))
        return
