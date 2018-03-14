from datetime import datetime, timedelta
from collections import namedtuple
from random import randint
from json import loads, dumps, load
from utils.web import Web
from utils.time import Time
class Utils:

    def __init__(self):

        self.help = "[INFO]"
        self.user = "[USER]"
        self.fail = "[FAIL]"
        self.message_encode = "utf-8"
        self.lennyfaces = self.get_lennyfaces()
        self.eightBall = self.get_eightball()
        self.starttime = datetime.now()
        self.time = Time()
        self.web = Web()

    def send(self, value, message):

        message = str(message.encode(self.message_encode))[2:-1]

        if value == 1:
            help_type = self.help
        elif value == 2:
            help_type = self.user
        elif value == 3:
            help_type = self.fail

        letter = str("{:[%Y-%m-%d %H:%M:%S.%f}".format(datetime.now())[:-3]+"]") + help_type + " " + message
        print(letter)



    def _json_object_hook(self, d):
        return namedtuple('X', d.keys())(*d.values())

    def json2obj(self, data):
        if data is None:
            return
        return loads(data, object_hook=self._json_object_hook)

    def open_file_json(self, file):

        with open(file, 'r', encoding="utf-8") as data:
            json_data = data.read().replace('\\', '\\\\')
            data.close()

        return self.json2obj(json_data)

    def get_modules_info(self):

        json_data = self.open_file_json('./maps/modules.json')

        return json_data

    def get_config_info(self):

        json_data = self.open_file_json('./maps/config.json')

        return json_data

    def get_lennyfaces(self):

        json_data = self.open_file_json('./maps/lennyfaces.json')

        return json_data

    def get_eightball(self):

        json_data = self.open_file_json('./maps/eight_ball.json')

        return json_data

    def time_now(self):

        return datetime.now()

    def author_nickanme(self, author):

        try:
            if author.nick is None:
                return author.name
            else:
                return author.nick
        except:
            return

    # Gives user instance
    async def get_user_instance(server, search):

        # Checking for part of the name
        for member in server.members:
            if search.lower() in member.name.lower():
                return member

        # Checking for part of the nick
        for member in message.server.members:
            try:
                if str(search).lower() in member.nick.lower():
                    return member
            except AttributeError:
                pass

        # Checking for users
        if search[:2] == "<@" and search[-1:] == ">" and search[2:-1].isnumeric():
            name = discord.utils.get(message.server.members, id=search[2:-1])
            return name

        # Checking for bots and selfnoti? and serverowner?
        if search[:3] == "<@!" and search[-1:] == ">" and search[3:-1].isnumeric():
            name = discord.utils.get(message.server.members, id=search[3:-1])
            return name

        # By id
        if len(search) == 18 and search.isnumeric():
            name = discord.utils.get(message.server.members, id=search)
            return name

            return
    def level_check(self, d_id, xp, level, level_base_xp, level_scaling_xp, level_scaling_max):

        response = self.level_xp(xp, level_base_xp, level_scaling_xp, level_scaling_max)
        rlist = []

        if response.new_level > level:
            response.set_level = True
            return response
        else:
            return response

    def level_xp(self, number, level_base_xp, level_scaling_xp, level_scaling_max, levl=0, result=0):

        while 1:
            result = self.level_from_xp(levl, level_base_xp, level_scaling_xp, level_scaling_max)
            if result > number:

                class Bedf:
                    def __init__(self, old_level, overleft_xp, new_level, set_level = False):

                        self.set_level = False
                        self.new_level = old_level
                        self.overleft_xp = overleft_xp
                        self.old_level = new_level

                return Bedf(levl, number, result)
            number = number - result
            levl += 1

    def level_from_xp(self, level, level_base_xp, level_scaling_xp, level_scaling_max):

        if level > level_scaling_max:
            level = level_scaling_max

        return level_base_xp + (level_scaling_xp * level)

class Timeout:

    timeouts = []
    command_timeouts = []

    async def user_msg(self, d_id):

        class Wsg:

            def __init__(self, d_id):
                self.d_id = d_id
                self.timestamp = datetime.now()

        Timeout.timeouts.append(Wsg(d_id))

    async def check_user_msg(self, d_id):

        for timeout in Timeout.timeouts:
            if timeout.d_id == d_id:
                if datetime.now() - timeout.timestamp < timedelta(seconds=60):
                    return True
        return False

    async def user_cmd_add(self, d_id, module):

        class Swg:

            def __init_(self, d_id, module):
                self.d_id = d_id
                self.module = module

        Timeout.command_timeouts.append(Swg(d_id, module))

    async def user_cmd_check(d_id, module):

        for cmdtimeout in Timeout.command_timeouts:
            if cmdtimeout.d_id == d_id and cmdtimeout.module == module:
                return True

        return False

    async def user_cmd_check_add(self, d_id, module):

        for cmdtimeout in Timeout.command_timeouts:
            if cmdtimeout.d_id == d_id and cmdtimeout.module == module:
                return True

        self.user_cmd_add(d_id, module)
        return False

    async def user_cmd_remove(self, d_id, module):

        for cmdtimeout in Timeout.command_timeouts:
            if cmdtimeout.d_id == d_id and cmdtimeout.module == module:
                Timeout.command_timeouts.remove(timeout)
