from urllib.request import quote
from bs4 import BeautifulSoup

class Youtube:

    # Iterating youtube results
    def get_yt_links(self, soup):

        # Lists to store links
        link_list = []
        name_list = []

        # Iterating for videos
        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            link_list.append('https://www.youtube.com' + vid['href'])
            name_list.append(vid["title"])

            # Wanted list length
            if len(link_list) >= 3:
                return link_list, name_list
            else:
                pass
        return link_list, name_list

    async def main(self, bot, database, message, arguments):

        # Creating youtube link
        url = "https://www.youtube.com/results?search_query="+quote(quote(arguments[0]))

        # Fetching link
        #response = urlopen(query)
        response = await bot.utils.web.get_content(url)
        #html = response.read()
        soup = BeautifulSoup(response, "lxml")

        # Finding source
        videos = self.get_yt_links(soup)

        # Creating message
        letter = ":arrow_forward: **| Here are some matches for: {}\n\n:one: | {}\n**<{}>**\n\n:two: | {}\n**<{}>**\n\n:three: | {}**\n<{}>"
        formation = letter.format(arguments[0], videos[1][0], videos[0][0], videos[1][1], videos[0][1], videos[1][2], videos[0][2])
        await bot.say(message.channel, formation)
