from discord import Embed

class DogPicture:

    async def get_dog_url(self, bot):

        for _ in range(5):
            json_data = await bot.utils.web.get_content("https://random.dog/woof.json")
            dog = bot.utils.json2obj(json_data)
            if "mp4" not in dog.url:
                return dog

    async def main(self, bot, database, message, arguments):

        dog = await self.get_dog_url(bot)

        name = bot.utils.author_nickanme(message.author)

        em=Embed(description=" ".format(name), colour=0xf99e1a)

        em.set_footer(text="Query by: {}".format(message.author.name))

        if dog is not None:
            letter = "{} here's a picture of a dog"
            em.set_image(url=dog.url)
        else:
            letter = "{} no dog found, please try again!"

        em.set_author(name=letter.format(name), icon_url=message.author.avatar_url)
        await bot.say(message.channel, embed=em)
