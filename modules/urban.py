from urllib.request import quote
from discord import Embed
class Urban:

    async def main(self, bot, database, message, arguments):

        # Getting site content
        url = "http://api.urbandictionary.com/v0/define?term={}".format(quote(arguments[0]))
        json_data = await bot.utils.web.get_content(url)
        urban = bot.utils.json2obj(json_data)

        em=Embed(description=urban.list[0].definition, colour=0xf99e1a)
        em.set_thumbnail(url="https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-01-11/297387706245_85899a44216ce1604c93_512.jpg")
        em.set_author(name="Definition of {}".format(arguments[0]), url=urban.list[0].permalink)
        em.add_field(name="Example", value=urban.list[0].example)
        em.add_field(name=":thumbsup: ", value=urban.list[0].thumbs_up)
        em.add_field(name=":thumbsdown: ", value=urban.list[0].thumbs_down)
        em.set_footer(text="Sent by {}".format(urban.list[0].author))

        await bot.say(message.channel, embed=em)
