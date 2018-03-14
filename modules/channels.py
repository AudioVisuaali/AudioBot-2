import asyncio

class ServerChannel:

    async def main(self, bot, database, message, arguments):

        roles_list, longest_name, number, numberlen, message_sent, first = "", 0, 0, 0, 0, True

        for role in message.server.roles:
            if len(role.name) > longest_name:
                longest_name = len(role.name)
            numberlen += 1


        for role in message.server.roles:
            number += 1
            roles_list += "[{}{}] {}{} ID: {} HEX: {}\n".format(str(number), " "*(len(str(numberlen))-len(str(number))), role.name, " "*(longest_name-len(role.name)), role.id, str(role.colour))
            message_sent = 0
            if len(roles_list) >= 1900:
                if first:
                    starter = "**Servers roles:**"
                    first = False
                else:
                    starter = ""
                roles_list = "{}```py\n{}```".format(starter, roles_list.replace("<","").replace(">",""))
                await bot.say(message.channel, roles_list)
                roles_list = ""
                message_sent = 1

        if message_sent == 0:
            if first:
                starter = "**Servers roles:**"
                first = False
            else:
                starter = ""
            roles_list = "{}```py\n{}```".format(starter, roles_list.replace("<","").replace(">",""))
        elif len(roles_list) > 2000:
            roles_list = "Internal server error!"

        await bot.say(message.channel, roles_list)
