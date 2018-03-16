from discord import Embed

class CatPicture:

    async def main(self, bot, database, message, arguments):

        json_data = await bot.utils.web.get_content("http://aws.random.cat/meow")

        name = bot.utils.author_nickanme(message.author)

        cat = bot.utils.json2obj(json_data)

        em=Embed(description=" ".format(name), colour=0xf99e1a)

        em.set_footer(text="Query by: {}".format(message.author.name))
        em.set_author(name="{} here's a picture of a cat".format(name), icon_url=message.author.avatar_url)
        em.set_image(url=cat.file)

        await bot.say(message.channel, embed=em)
