class Help:

    async def main(self, bot, database, message, arguments):

        starter = bot.database.server.get(message.server.id).command_start
        if not arguments:
            keepo = "**Here are all the commands!!!**\n"
            func_cmd_list = []
            admin_cmd_list = []

            for module in bot.modules:
                if module.owner == False:
                    func_cmd_list.append(starter + module.call)
                else:
                    admin_cmd_list.append(starter + module.call)

            keepo += "`{}`".format(", ".join(func_cmd_list))
            react = bot.database.command.get_all_server(message.server.id)

            if react != []:
                keepo += "\n\n**Here are all the custom commands!!**\n"
                keepo += "`" + ", ".join(starter + b.command for b in react) + "`"

            try:
                if message.author.id in message.server.owner.id:
                    keepo += "\n\n**Here are all the __ADMIN__ commands!!!** :smirk:\n"
                    keepo += "`{}`".format(", ".join(admin_cmd_list))
            except:
                pass

            keepo += "\n\nFor more help do {}help <command>".format(starter)
            await bot.say(message.channel, keepo)

        else:
            for module in bot.modules:
                if module.call == arguments[0]:
                    mail = ""
                    all_alias = ""
                    for example_ in module.exmaple:
                        mail += "\n__Input:__ {}{}\n__Output:__ {}\n".format(starter, example_.input, example_.output)

                    if module.aliases:
                        all_alias = ", ".join(["{}{}".format(starter, x) for x in module.aliases])
                        
                    letter = "**:question: | Help menu for {}\n\n__INFO:__ {}\n__SYNTAX:__ {}{}\n__ALIASES:__ {}\n{}**".format(module.call, module.info, starter, module.syntax, all_alias, mail)
                    await bot.say(message.channel, letter)
