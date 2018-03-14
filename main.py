from discord import Client
from database.database import Database
from utils import Utils, Timeout
from random import randint
from asyncio import sleep as asleep
import modules

database = Database()

class Bot(Client):

    def __init__(self):

        Client.__init__(self)

        self.utils = Utils()
        self.timeout = Timeout()

        self.send = self.utils.send
        self.modules = self.utils.get_modules_info()
        self.config = self.utils.get_config_info()
        self.start_time = self.utils.time_now()
        self.say = self.send_message

        return

    def start_bot(self):

        # Try to start bot
        try:
            self.loop.run_until_complete(self.start(self.config.bot.token))

        # Check for KeyboardInterrupt
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())
            database.bot.close()
            database.dispose()

        # If KeyboardInterrupt stop bot and close stuff
        finally:
            self.loop.close()
            print("Bot has been closed")

        return

    # Bot has connected to discord
    async def on_ready(self):

        self.send(1, "Logged in as: {}".format(self.user.name))
        self.send(1, "Client ID: {}".format(self.user.id))
        self.send(1, "Listening to the chat!")

        return

    async def on_member_join(self, member):

        server_exists = database.server.exists(member.server.id)

        if not server_exists:
            database.server.add(member.server.id)

        server_info = database.server.get(member.server.id)

        if server_info.welcome_channel != None:

            channel = self.get_channel(server_info.welcome_channel)
            letter = server_info.welcome_message

            if letter != "":
                await self.send_message(channel, letter.format(member.name, member.server.name)) #{0=username} {1=servername}

        if server_info.welcome_private:

            letter = server_info.welcome_private_message

            if letter != "":
                await self.send_message(member, letter.format(member.name)) #{0=username}

        return

    async def on_member_remove(self, member):

        server_info = database.server.get_from_server_aut_add(member.sesrver)

        name = self.utils.author_nickanme(member)

        if server_info.goodbye_channel != None:

            channel = self.get_channel(server_info.goodbye_channel)
            letter = server_info.goodbye_message

            if letter != "":
                await self.send_message(channel, letter.format(member.name, member.nick, name, member.server.name)) #{0=username} {1=usernick} {2=nick then name}{3=servername}

        return

    async def on_message_delete(self, message):

        database.message.delete(message)

        return

    async def on_message_edit(self, before, after):

        return

    async def get_module(self, module_name):

        for module in self.modules:
            if module_name == module.call or module_name in module.aliases:
                return module

    async def import_module(self, name):
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    async def filter_module(self, message, database, server_stats):

        if not message.content.startswith(server_stats.command_start):
            return

        content = message.content.replace(server_stats.command_start, "", 1)
        try:
            command, args = content.split(" ", 1)
        except:
            command = content
            args = None
        finally:
            class_name_, arguments = "", []

        # Check if cd, if not -> add
        if await self.timeout.user_cmd_check_add(message.author.id, command):
            return

        module = await self.get_module(command)

        if module is None:
            class_name_ = "GetCommand"
            arguments = command

        else:
            if module.owner:
                if message.author.id != message.server.owner.id:
                    return

            class_name_ = module.class_name

            if module.args.delimeter is None:
                if args != None:
                    arguments.append(args)

                if not(len(arguments) in module.args.length):
                    return

            elif module.args.delimeter is not None:
                if args:
                    arguments.extend(args.split(module.args.delimeter, module.args.split))

                if len(arguments) not in module.args.length:
                    return

        class_ = getattr(modules, class_name_)()
        await class_.main(self, database, message, arguments)

        # Remove cd
        await asleep(1)
        await self.timeout.user_cmd_remove(message.author.id, command)

    async def on_message(self, message):
        """Doesn't really like private messages yet"""
        name = self.utils.author_nickanme(message.author)

        self.send(1, "{} > {}".format(name, message.content))

        database.message.add(message)

        if message.channel.is_private:
            #TODO ADD HELP MODULE HERE
            return

        user_stats = database.user.get_from_msg_aut_add(message)
        server_stats = database.server.get_from_server_aut_add(message.server)
        bot_stats = database.bot.get()

        if message.content.startswith(server_stats.command_start):
            points_amount = randint(bot_stats.cmd_point_min, bot_stats.cmd_point_max)
            xp_amount = randint(bot_stats.cmd_xp_min, bot_stats.cmd_xp_max)
        else:
            points_amount = randint(bot_stats.msg_point_min, bot_stats.msg_point_max)
            xp_amount = randint(bot_stats.msg_xp_min, bot_stats.msg_xp_max)

        messages_active = await self.timeout.check_user_msg(message.author.id)

        if not messages_active:

            database.user.points_alter(message.author.id, points_amount)
            database.user.xp_alter(message.author.id, xp_amount)
            await self.timeout.user_msg(message.author.id)

        levels = self.utils.level_check(message.author.id, user_stats.xp, user_stats.level,
                                        bot_stats.level_base_xp, bot_stats.level_scaling_xp,
                                        bot_stats.level_scaling_max)
        if levels.set_level:
            database.user.level_alter(message.author.id, 1)

            if server_stats.post_level:
                letter = server_stats.post_level_msg

                if server_stats.post_level_same_channel_as_msg:
                    await self.send_message(message.channel, letter.format(name, levels.new_level))

                else:
                    channel = self.get_channel(server_info.post_info_channel)
                    await self.send_message(channel, letter.format(name, levels.new_level))

        if message.author.id == self.user.id:
            return

        await self.filter_module(message, database, server_stats)

        return
