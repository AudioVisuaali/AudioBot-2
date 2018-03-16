from urllib.request import quote

class Osu:

    async def main(self, bot, database, message, arguments):

        url = "https://osu.ppy.sh/api/get_user?u={}&k={}".format(quote(arguments[0]), bot.config.osu.key)
        json_data = await bot.utils.web.get_content(url)
        osu = bot.utils.json2obj(json_data)

        if not osu:
            return

        send = "Osu stats for "+osu[0].username+"```PP"+" "*12+str(round(float(osu[0].pp_raw)))+" PP\nLevel"+" "*9+str(round(float(osu[0].level),1))+" lvl\nGlobal rank"+" "*3+osu[0].pp_rank+"\nCountry rank"+" "*2+osu[0].pp_country_rank+"\nCountry"+" "*7+osu[0].country+"\nAccuracy"+" "*6+str(round(float(osu[0].accuracy), 2))+" %\nRanked Score"+" "*2+osu[0].ranked_score+"\nTotal Score"+" "*3+osu[0].total_score+"```"
        await bot.say(message.channel, "<@"+message.author.id+"> "+send)
