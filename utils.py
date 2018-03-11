from datetime import datetime, timedelta
from collections import namedtuple
from json import loads
import asyncio

class Utils:

    def __init__(self):

        self.help = "[INFO]"
        self.user = "[USER]"
        self.fail = "[FAIL]"
        self.message_encode = "utf-8"


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
        return loads(data, object_hook=self._json_object_hook)

    def get_modules_info(self):

        with open('./maps/modules.json', 'r') as data:
            json_data = data.read()
            data.close()

        return self.json2obj(json_data)

    def get_config_info(self):

        with open('./maps/config.json', 'r') as data:
            json_data = data.read()
            data.close()

        return self.json2obj(json_data)

    def time_now(self):

        return datetime.now()

    def author_nickanme(self, author):

        if author.nick is None:
            return author.name
        else:
            return author.nick

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
        Timeout.command_timeouts.append("{}:{}".format(d_id, module))

    async def user_cmd_check(d_id, module):
        for cmdtimeout in Timeout.command_timeouts:
            if cmdtimeout == "{}:{}".format(d_id, module):
                return True
        return False

    async def user_cmd_check_add(self, d_id, module):
        for cmdtimeout in Timeout.command_timeouts:
            if cmdtimeout == "{}:{}".format(d_id, module):
                return True

        Timeout.command_timeouts.append("{}:{}".format(d_id, module))
        return False

    async def user_cmd_remove(self, d_id, module):
        Timeout.command_timeouts.remove("{}:{}".format(d_id, module))
