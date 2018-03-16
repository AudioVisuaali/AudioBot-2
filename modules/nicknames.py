class UserNickNames:

    async def main(self, bot, database, message, arguments):

        owner = message.author
        nicks = []

        nicks.append(owner.name)
        nicknames = bot.database.nickname.get_user_nicks(owner.id)

        for nick in nicknames:
            if nick.nickname_before not in nicks and nick.nickname_before is not None:
                nicks.append(nick.nickname_before)
            if nick.nickname_after not in nicks and nick.nickname_after is not None:
                nicks.append(nick.nickname_after)

        if owner.nick not in nicks and owner.nick is not None:
            nicks.append(owner.nick)

        letter = "Nicknames: {}".format(", ".join(nicks))
        await bot.say(message.channel, letter)
