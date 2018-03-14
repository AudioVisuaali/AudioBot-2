class Wikipedia:

    async def main(self, bot, database, message, arguments):

        name = bot.utils.author_nickanme(message.author)
        sites = ""

        query = "https://en.wikipedia.org/w/api.php?action=query&list=search&utf8=&format=json&srsearch={}".format(arguments[0])

        json_data = await bot.utils.web.get_content(query)

        json_data = json_data.replace("continue", "carryon")

        wiki = bot.utils.json2obj(json_data)

        letter = ":bookmark: **| {}, here's your link for: **__{}__\n".format(name, arguments[0])

        try:
            letter += "\n:one: **<https://en.wikipedia.org/wiki/{}>**\n{}\n".format(wiki.query.search[0].title.replace(" ", "_"), self.format(wiki.query.search[0].snippet))
            try:
                letter += "\n:two: **<https://en.wikipedia.org/wiki/{}>**\n{}\n".format(wiki.query.search[1].title.replace(" ", "_"), self.format(wiki.query.search[1].snippet))
                try:
                    letter += "\n:three: **<https://en.wikipedia.org/wiki/{}>**\n{}\n".format(wiki.query.search[2].title.replace(" ", "_"), self.format(wiki.query.search[2].snippet))
                except: pass
            except: pass
        except:
            letter = ":bookmark: **| {}, we couldn't find a match!**".format(name)

        await bot.say(message.channel, letter)

    def format(self, msg):

        letter = msg.replace("</span>", "**").replace('<span class="searchmatch">', "**").replace("&quot;", '"')

        return letter
