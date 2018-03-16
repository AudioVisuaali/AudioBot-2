from math import floor as mfloor

class GetXp:

    async def main(self, bot, database, message, arguments):

        if len(arguments) != 0:
            user = await bot.utils.get_user_instance(message.server, arguments[0])

            if user is None:
                await bot.say(message.channel, ":chart_with_upwards_trend: **| User not found!**")
                return
        else:
            user = message.author

        owner = bot.database.user.get(user.id)
        name = bot.utils.author_nickanme(user)

        levels = bot.utils.level_xp(owner.xp, 2000, 200, 40)
        progress = str(mfloor((levels.overleft_xp / levels.levels_xp)*100))

        letter = ":chart_with_upwards_trend: **| {} is level {} and has {} xp in total! {}% done on the current level!**".format(name, levels.new_level, owner.xp, progress)
        await bot.say(message.channel, letter)
