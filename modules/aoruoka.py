from datetime import datetime
from bs4 import BeautifulSoup
from random import randint

class AoRuoka:

    async def main(self, bot, database, message, arguments):

        # Variables
        food, add_food_with_this, letter, count = [], [], "", 0

        # PAge address
        page = await bot.utils.web.get_content("https://www.jao.fi/fi/Jyvaskylan-koulutuskuntayhtyma/Asiakaspalvelut/Palvelut-Jyvaskylassa/Opiskelijaravintolat/Lounastuuli")
        soup = BeautifulSoup(page, "lxml")
        kappa = soup.find_all("div", {"class": "day"})

        # for each day in week
        for asd in kappa:

            # Adding weekday
            KEEPO = asd.find("span", {"class": "dayname"})
            KAPPA = KEEPO.text.title()
            add_food_with_this.append("__" + KAPPA + "__:")

            # For each lunch in day
            for auto in asd.find_all("span", {"class": "lunch"}):
                auto = auto.text
                add_food_with_this.append(auto)

            # add day
            food.append(add_food_with_this)
            add_food_with_this = []

        if len(arguments) == 0:
            # Format
            for weekday in food:

                # Indent if todays food
                wrapper = ""
                if datetime.today().weekday() == count and count < 5:
                    wrapper = "**"

                    # Wrapping
                    letter += wrapper + "\n".join(weekday) + wrapper + "\n\n__{}ao week__ for the whole week!".format(bot.database.server.get(message.server.id).command_start)
                elif datetime.today().weekday() >= 5 and count == 5:
                    letter += wrapper + "\n".join(weekday) + wrapper + "\n\nThis is for the next weeks mondays food!\n__{}ao week__ for the whole week!".format(bot.database.server.get(message.server.id).command_start)
                count += 1

        else:
            # Format
            for weekday in food:

                # Indent if todays food
                if count == 5:
                    letter += "**=====================\n\n**"

                # Wrapping
                letter += "\n".join(weekday) + "\n\n"
                count += 1

        # Send message
        if not letter == "":
            await bot.say(message.channel, letter)

    # def get_food_for_main(self,bot):
    #
    #         # Variables
    #         food, add_food_with_this, letter, count = [], [], "", 0
    #
    #         # PAge address
    #         page = await bot.utils.web.get_content("https://www.jao.fi/fi/Jyvaskylan-koulutuskuntayhtyma/Asiakaspalvelut/Palvelut-Jyvaskylassa/Opiskelijaravintolat/Lounastuuli")
    #         soup = BeautifulSoup(page.content, "lxml")
    #         kappa = soup.find_all("div", {"class": "day"})
    #
    #         # for each day in week
    #         for asd in kappa:
    #
    #             # Adding weekday
    #             dayname = asd.find("span", {"class": "dayname"})
    #             dayname_title = dayname.text.title()
    #             add_food_with_this.append("__{}__:".format(dayname_title))
    #
    #             # For each lunch in day
    #             for auto in asd.find_all("span", {"class": "lunch"}):
    #                 auto = auto.text
    #                 add_food_with_this.append(auto)
    #
    #             # add day
    #             food.append(add_food_with_this)
    #             add_food_with_this = []
    #
    #                 # Format
    #         for weekday in food:
    #
    #                     # Indent if todays food
    #             if datetime.today().weekday() < 5:
    #                 wrapper = ""
    #
    #                 if datetime.today().weekday() == count:
    #                     wrapper = "**"
    #
    #                     # Wrapping
    #                     letter += wrapper + "\n".join(weekday) + wrapper + "\n\n"
    #             count += 1
    #
    #         # Send message
    #         #await bot.say(message.channel, letter)
    #
    #         if not letter == "":
    #             return "{}".format(letter)
