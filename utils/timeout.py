from datetime import datetime, timedelta

class Timeout:

    def __init__(self):
        self.timeouts = []
        self.command_timeouts = []
        self.roll_timeout = []

    async def user_msg(self, d_id):

        class Wsg:

            def __init__(self, d_id):
                self.d_id = d_id
                self.timestamp = datetime.now()

        self.timeouts.append(Wsg(d_id))

    async def check_user_msg(self, d_id):

        for timeout in self.timeouts:
            if timeout.d_id == d_id:
                if datetime.now() - timeout.timestamp < timedelta(seconds=60):
                    return True
        return False

    async def add_roll(self, d_id):

        class Wsg:

            def __init__(self, d_id):
                self.d_id = d_id
                self.timestamp = datetime.now()

        self.timeouts.append(Wsg(d_id))

    async def check_roll(self, d_id):

        for roll in self.roll_timeout:
            if roll.d_id == d_id:
                if datetime.now() - roll.timestamp < timedelta(seconds=60):
                    return True
        return False

    async def user_cmd_add(self, d_id, module):
        self.command_timeouts.append("{}:{}".format(d_id, module))

    async def user_cmd_check(d_id, module):
        for cmdtimeout in self.command_timeouts:
            if cmdtimeout == "{}:{}".format(d_id, module):
                return True
        return False

    async def user_cmd_check_add(self, d_id, module):
        for cmdtimeout in self.command_timeouts:
            if cmdtimeout == "{}:{}".format(d_id, module):
                return True

        self.command_timeouts.append("{}:{}".format(d_id, module))
        return False

    async def user_cmd_remove(self, d_id, module):
        try:
            self.command_timeouts.remove("{}:{}".format(d_id, module))
        except:
            pass
    def delete_timeouts(self, total = 0):

        total += len(self.timeouts)
        total += len(self.command_timeouts)
        total += len(self.roll_timeout)

        self.timeouts = []
        self.command_timeouts = []
        self.roll_timeout = []

        return total
