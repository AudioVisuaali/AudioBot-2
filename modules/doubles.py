from math import floor as mfloor

class Doubles:

    async def main(self, bot, database, message, arguments):

        if len(arguments) == 0:
            owner = message.author
        else:
            owner = await bot.utils.get_user_instance(message.server, arguments[0])

        stats = bot.database.double.get_stats_user(owner.id)

        if stats is None:
            return

        name = bot.utils.author_nickanme(owner)
        user_mention = " for: " + name

        # Calculating winrate
        try:
            win_rate = mfloor(int(stats.doubles) / int(stats.rows) * 100)
        except:
            win_rate = "0"

        if stats.memes == 0:
            memes = ""
        else:
            try:
                memes = "\n:money_with_wings: Memes gained: {}".format(mfloor(stats.memes))
            except:
                memes = ""

        if stats.tokens == 0:
            tokens = ""
        else:
            try:
                tokens = "\n:trophy: Tokens gained: {}".format(mfloor(stats.tokens))
            except:
                tokens = ""

        letter = ":game_die: **| Roll stats{}\n\n:arrows_counterclockwise: Rolled: {}\n:tada: Doubles: {}\n:thinking: Win-rate: {}%{}{}**".format(user_mention, stats.rows, stats.doubles, win_rate, memes, tokens)
        await bot.say(message.channel, letter)
