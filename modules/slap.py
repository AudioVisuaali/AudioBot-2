class Slap:

    async def main(self, bot, database, message, arguments):

        #user = bot.utils.author_nickanme(arguments[0])
        if user is None: return

        # Creating author name
        author_name = author_nickanme(message.author)

        # Creating clients name
        client_name = author_nickanme(user)

        # Sending message
        letter = "**:raised_back_of_hand: | {} sla:b:s {}!**".format(author_name, client_name)
        await client.send_message(message.channel, letter)
