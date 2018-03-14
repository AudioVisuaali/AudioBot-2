from urllib.request import quote

class Trump:

    async def main(self, bot, database, message, arguments):

        query = "https://api.tronalddump.io/search/quote?query={}".format(quote(arguments[0]))
        json_data = await bot.utils.web.get_content(query)

        json_data = json_data.replace("_embedded", "embedded").replace("_links", "links")
        trump = bot.utils.json2obj(json_data)

        if trump == None or trump.total == 0:
            letter = ":rofl: **| No quotes found!**"

        else:
            hits = ""
            for asd in trump.embedded.quotes:
                hits += "```{}```".format(asd.value)
                
            letter = ":rofl: **| Found {} hits**\n{}".format(trump.total, hits)

        await bot.say(message.channel, letter)
