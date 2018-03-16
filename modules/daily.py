from datetime import datetime
from random import randint

class Daily:

    async def main(self, bot, database, message, arguments):

        day = bot.utils.time.day_splitted_by_time(46800)
        redeems = bot.database.redeem.check_daily(message.author.id, day)
        user_points = bot.database.user.get(message.author.id).points

        miscalc = randint(0,100)
        amount = randint(bot.database.cache.botinfo.daily_min, bot.database.cache.botinfo.daily_max)
        if miscalc < 1:
            amount = amount * 4
            extra = ", __miscalculation happened you gained fourfold to normal__"
            info1 = "miscalculation"
            info2 = "4x"
        elif miscalc < 5:
            amount = amount * 2
            extra = ", __miscalculation happened you gained twofold to normal__"
            info1 = "miscalculation"
            info2 = "2x"
        else:
            amount = amount
            extra = ""
            info2 = ""
            info1 = ""

        # name
        name = bot.utils.author_nickanme(message.author)

        # Message
        if not redeems:
            await bot.say(message.channel, ":moneybag: **| You redeemed your daily points worth of {} memes{}! You now have {} memes!**".format(amount, extra, user_points + amount))
            bot.database.pointhistory.add(message.author.id, message.server.id, 2, "Daily", False, "", "", "+"+str(amount), "", info1, info2, "", "", 0, amount, 0)

            try:
                bot.database.redeem.add(message.author.id, day, amount)
            except:
                pass
            finally:
                bot.database.user.points_alter(message.author.id, amount)
        else:
            await bot.say(message.channel, ":moneybag: **| Check again when the clock is `15:00`**")
