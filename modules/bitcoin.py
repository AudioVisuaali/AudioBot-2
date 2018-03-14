from discord import Embed

class Bitcoin:

    async def main(self, bot, database, message, arguments):

        # Getting site content
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        json_data = await bot.utils.web.get_content(url)
        coin = bot.utils.json2obj(json_data)

        if coin is None:
            return

        # Value
        usd = "%.2f" % coin.bpi.USD.rate_float
        gbp = "%.2f" % coin.bpi.GBP.rate_float
        eur = "%.2f" % coin.bpi.EUR.rate_float

        # embed
        em=Embed(description="USD: ${}\nGBP: £{}\nEUR: €{}".format(usd, gbp, eur), colour=0xf99e1a)
        em.set_author(name="Bitcoin is worth", icon_url="http://icons.iconarchive.com/icons/froyoshark/enkel/256/Bitcoin-icon.png")
        await bot.say(message.channel, embed=em)
