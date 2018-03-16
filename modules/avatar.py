from discord import Embed

class Avatar:

    async def main(self, bot, database, message, arguments):

        # Checks if message author or else
        if arguments:
            user = await bot.utils.get_user_instance(message.server, arguments[0])
            if user is None:
                return
        else:
            user = message.author

        name = bot.utils.author_nickanme(user)

        em=Embed(description=" ".format(name), colour=0xf99e1a)

        em.set_footer(text="Query by: {}".format(message.author.name))
        em.set_author(name="{}s' profile picture".format(name), icon_url=user.avatar_url)
        em.set_image(url=user.avatar_url)

        await bot.say(message.channel, embed=em)
