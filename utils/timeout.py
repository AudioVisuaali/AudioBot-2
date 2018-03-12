from datetime import datetime, timedelta

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
