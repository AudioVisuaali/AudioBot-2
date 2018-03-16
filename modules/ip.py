from socket import gethostbyname
from urllib.request import quote

class ResolveIp:

    async def main(self, bot, database, message, arguments):

        ip_address = gethostbyname(arguments[0])

        url = "https://ipinfo.io/{}/json".format(quote(ip_address))

        json_data = await bot.utils.web.get_content(url)

        ip = bot.utils.json2obj(json_data)

        letter = ":printer:  **| We found info for your ip! ```IP: {}\ncity: {}\nregion: {}\ncountry: {}\nloc: {}\norg: {}```**".format(ip.ip, ip.city, ip.region, ip.country, ip.loc, ip.loc)

        await bot.say(message.channel, letter)
