from urllib.request import quote

from re import search as rsearch
from re import sub as rsub

class Translate:

    async def main(self, bot, database, message, arguments):

        #Cheking if input contains any arguments DO NOT TOUCH WAS PAIN
        try:
            popped = rsearch("--([a-zA-Z0-9])\w+", arguments[0]).group()
        except AttributeError:
            google = quote(str(arguments[0]))
            language = "en"
        else:
            google = quote(str(rsub(r"--([a-zA-Z0-9])\w+", "", arguments[0])))
            language = popped[2:]

        url = "https://translation.googleapis.com/language/translate/v2?key={}&target={}&q={}".format(bot.config.google.key, language, google)

        json_data = await bot.utils.web.get_content(url)

        translate = bot.utils.json2obj(json_data)
        print(json_data)
        # Trying to create message
        try:
            detectedlanguage = translate.data.translations[0].detectedSourceLanguage# response["data"]["translations"][0]["detectedSourceLanguage"]
            translatedtext = translate.data.translations[0].translatedText#    response["data"]["translations"][0]["translatedText"]
            letter = ":cloud:  **| " + detectedlanguage.upper() + " -> " + language.upper() + "  `" + translatedtext + "`**"

        # if can't create mesage rteturn error
        except KeyError:
            letter = ":cloud:  **| Invalid language target!**"

        # sending message
        await bot.say(message.channel, letter)
