from sqlalchemy import (Table, Column, Integer,
                        Date, select, literal, and_,
                        exists, create_engine, update)
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.sql import exists, and_
from utils.decorators import Commit, IsBoolean, IsInteger, IsString
from database.tables import (Servers, Users, Messages,
                             PointHistory, Commands, BotInfo,
                             Base)
from utils import Utils

util = Utils()
config = util.get_config_info()

# Create engine
addr = '{0.type}://{0.username}:{0.password}@{0.address}/{0.database}'.format(config.database)
engine = create_engine(addr, echo=False, convert_unicode=True)

# Create tables
Base.metadata.create_all(engine)

# Database connector
class Database:

    def __init__(self):

        DatabaseConntection.__init__(self)
        self.user = User()
        self.server = Server()
        self.message = Message()
        self.points = Points()
        self.bot = Bot()
        self.command = Command()
        self.cache = Cache()

        Cache.get_cache(self)

    def getEngine(self):

        return self.engine

    def dispose(self):

        engine.dispose()

# Connection
class DatabaseConntection:

    # Create connection
    def __init__(self):

        # Create session
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.connection = engine.connect()

        return

    def close(self):

        self.close()

class Cache(DatabaseConntection):

    users = []
    servers = []
    commands = []
    module_timeouts = []
    botinfo = None

    def get_cache(self):

        for server in Server.get_all(self):
            Cache.servers.append(server)

        for user in User.get_all(self):
            Cache.users.append(user)

        for command in Command.get_all(self):

            Cache.commands.append(command)

        botstats = Bot.get_all(self)
        if not botstats:
            Bot.add(self, total_restarts = 0, cmd_xp_max = 15, cmd_xp_min = 15, msg_xp_max = 25, msg_xp_min = 15)
        else:
            Cache.botinfo = botstats[0]
        return

# User
class User(DatabaseConntection):

    @Commit
    def add(self, author, points=0, bank=0, xp=0, level=0, tokens=0):

        useradd = Users(author.id, points, bank, xp, level, tokens)

        Cache.users.append(useradd)
        self.session.add(useradd)

        return useradd

    def get_all(self):

        return self.session.query(Users).all()

    def exists(self, d_id):

        for user in Cache.users:
            if user.d_id == d_id:
                return True

        return False

    def get(self, d_id):

        for user in Cache.users:
            if user.d_id == d_id:
                return user

        return None

    def get_from_msg_aut_add(self, message):

        for user in Cache.users:
            if user.d_id == message.author.id:
                return user

        useradd = self.add(message.author)

        return useradd

    @IsInteger
    def points_alter(self, d_id, point_amount):

        for user in Cache.users:
            if user.d_id == d_id:
                user.points += point_amount

        stmt = update(Users).where(Users.d_id == d_id).\
                values(points = Users.points + point_amount)

        self.connection.execute(stmt)

        return

    @IsInteger
    def bank_alter(self, d_id, point_amount):

        for user in Cache.users:
            if user.d_id == d_id:
                user.bank += point_amount

        stmt = update(Users).where(Users.d_id == d_id).\
                values(bank = Users.bank + point_amount)

        self.connection.execute(stmt)

        return

    @IsInteger
    def xp_alter(self, d_id, xp_amount):

        for user in Cache.users:
            if user.d_id == d_id:
                user.xp += xp_amount

        stmt = update(Users).where(Users.d_id == d_id).\
                values(xp = Users.xp + xp_amount)

        self.connection.execute(stmt)

        return

    @IsInteger
    def level_alter(self, d_id, level_amount):

        for user in Cache.users:
            if user.d_id == d_id:
                user.level += level_amount

        stmt = update(Users).where(Users.d_id == d_id).\
                values(level = Users.level + level_amount)

        self.connection.execute(stmt)

        return

    @IsInteger
    def level_set(self, d_id, level_set):

        for user in Cache.users:
            if user.d_id == d_id:
                user.level = level_set

        stmt = update(Users).where(Users.d_id == d_id).\
                values(level = level_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def tokens_alter(self, d_id, tokens_amount):

        for user in Cache.users:
            if user.d_id == d_id:
                user.tokens += tokens_amount

        stmt = update(Users).where(Users.d_id == d_id).\
                values(tokens = Users.tokens + tokens_amount)

        self.connection.execute(stmt)

        return

# Server
class Server(DatabaseConntection):

    @Commit
    def add(self, server, command_start="!",
            tax_pot=0, msg_point_max=2, msg_point_min=2,
            msg_xp_max=25, msg_xp_min=15, cmd_point_max=1,
            cmd_point_min=1, cmd_xp_max=15, cmd_xp_min=15,
            level_base_xp = 2000, level_scaling_xp= 200, level_scaling_max = 40,
            post_level=False, post_level_msg = "{0} is now level {1}", post_level_same_channel_as_msg=False,
            post_info_channel=None, casino_state=False, welcome_channel=None,
            welcome_message="Welcome to the server {0}!", welcome_private=False, welcome_private_message=None,
            goodbye_channel=None, goodbye_message="{3} left the server, hold those memories!"):

        serveradd = Servers(server.id, command_start, tax_pot,
                            msg_point_max, msg_point_min, msg_xp_max,
                            msg_xp_min, cmd_point_max, cmd_point_min,
                            cmd_xp_max, cmd_xp_min, level_base_xp,
                            level_scaling_xp, level_scaling_max, post_level,
                            post_level_msg, post_level_same_channel_as_msg, post_info_channel,
                            casino_state, welcome_channel, welcome_message,
                            welcome_private, welcome_private_message, goodbye_channel,
                            goodbye_message)

        Cache.servers.append(serveradd)
        self.session.add(serveradd)

        return serveradd

    def get_all(self):

        return self.session.query(Servers).all()

    def exists(self, server_id):

        for server in Cache.servers:
            if server.server_id == server_id:
                return True

        return False

    def get(self, server_id):

        for server in Cache.servers:
            if server.server_id == server_id:
                return server

        return None

    def get_from_server_aut_add(self, server):

        for servers in Cache.servers:
            if servers.server_id == server.id:
                return servers

        serveradd = self.add(server)

        return serveradd

    @IsString
    def command_start_set(self, server_id, command_starter):

        for server in Cache.servers:
            if server.server_id == server_id:
                server.command_start = command_starter

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(command_start = command_starter)

        self.connection.execute(stmt)

        return

    @IsInteger
    def tax_pot_alter(self, server_id, alter_tax_pot):

        for server in Cache.servers:
            if server.server_id == server_id:
                server.tax_pot = alter_tax_pot

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(tax_pot = alter_tax_pot)

        self.connection.execute(stmt)

        return

    @IsInteger
    def msg_point_max_set(self, server_id, point_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.msg_point_max = point_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(msg_point_max = point_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def msg_point_min_set(self, server_id, point_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.msg_point_min = point_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(msg_point_min = point_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def msg_xp_max_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.msg_xp_max = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(msg_xp_max = xp_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def msg_xp_min_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.msg_xp_min = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(msg_xp_min = xp_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def cmd_point_max_set(self, server_id, point_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.cmd_point_max = point_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(cmd_point_max = point_set)

        self.connection.execute(stmt)

    @IsInteger
    def cmd_point_min_set(self, server_id, point_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.cmd_point_min = point_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(cmd_point_min = point_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def cmd_xp_max_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.cmd_xp_max = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(cmd_xp_max = xp_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def cmd_xp_min_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.cmd_xp_min = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(cmd_xp_min = xp_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def level_base_xp_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.level_base_xp = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(level_base_xp = xp_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def level_scaling_xp_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.level_scaling_xp = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(level_scaling_xp = xp_set)

        self.connection.execute(stmt)

        return

    @IsInteger
    def level_scaling_max_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.level_scaling_max = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(level_scaling_max = xp_set)

        self.connection.execute(stmt)

        return

    @IsBoolean
    def post_level_set(self, server_id, boolean_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.post_level = boolean_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(post_level = boolean_set)

        self.connection.execute(stmt)

        return

    @IsString
    def post_level_msg_set(self, server_id, level_msg):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.post_level_msg = level_msg

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(post_level_msg = level_msg)

        self.connection.execute(stmt)

        return

    @IsBoolean
    def post_level_same_channel_as_msg_set(self, server_id, boolean_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.post_level_same_channel_as_msg = boolean_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(post_level_same_channel_as_msg = boolean_set)

        self.connection.execute(stmt)

        return

    @IsString
    def post_info_channel_set(self, server_id, channel_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.post_info_channel = channel_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(post_info_channel = channel_set)

        self.connection.execute(stmt)

        return

    @IsBoolean
    def casino_state_set(self, server_id, state_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.casino_state = state_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(casino_state = state_set)

        self.connection.execute(stmt)

        return

    @IsString
    def welcome_channel_set(self, server_id, channel_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.welcome_channel = channel_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(welcome_channel = channel_set)

        self.connection.execute(stmt)

        return

    @IsString
    def welcome_message_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.welcome_message = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(welcome_message = message_set)

        self.connection.execute(stmt)

        return

    @IsBoolean
    def welcome_private_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.welcome_private = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(welcome_private = message_set)

        self.connection.execute(stmt)

        return

    @IsString
    def welcome_private_message_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.welcome_private_message = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(welcome_private_message = message_set)

        self.connection.execute(stmt)

        return

    @IsString
    def goodbye_channel_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.goodbye_channel = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(goodbye_channel = message_set)

        self.connection.execute(stmt)

        return

    @IsString
    def goodbye_message_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.goodbye_message = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(goodbye_message = message_set)

        self.connection.execute(stmt)

        return

class Message(DatabaseConntection):

    @Commit
    def add(self, message, deleted=False):

        images = True
        private = True
        message_server_id = None

        if not message.attachments:
            images = False

        if not message.channel.is_private:
            private = False
            message_server_id = message.server.id

        messageadd = Messages(message.author.id, message_server_id, message.channel.id,
                     message.id, message.content, private,
                     images, deleted)

        self.session.add(messageadd)

        return

    def on_new(self, server_id, d_id):

            a, b =  self.session.query(exists().where(Servers.server_id == server_id), exists().where(Users.d_id == d_id)).all()[0]

            class kek:
                def __init__(self, isserver, isuser):
                    self.server = isserver
                    self.user = isuser

            return kek(a, b)

    def delete(self, message):

        private = True
        server_id = None
        message_id = message.id
        channel_id = message.channel.id

        if not message.channel.is_private:
            private = False
            server_id = message.server.id

        stmt = update(Messages).where(and_(Messages.server_id == server_id,
                                           Messages.room_id == channel_id,
                                           Messages.message_id == message_id,
                                           Messages.private == private)).\
                values(deleted = True)

        self.connection.execute(stmt)

        return

class Points(DatabaseConntection):

    @Commit
    def add(self, d_id, server_id, mode_id,
            mode_name, private=False, stake_points=0, stake_tokens=0,
            outcome_points=0, outcome_tokens=0, info1=None,
            info2=None, info3=None, info4h=None,
            info5h=0, plus=0, minus=0):

        pointsadd = PointHistory(d_id, server_id, mode_id,
                    mode_name, private, stake_points, stake_tokens,
                    outcome_points, outcome_tokens, info1,
                    info2, info3, info4h,
                    info5h, plus, minus)

        self.session.add(pointsadd)

        return


class Bot(DatabaseConntection):

    @Commit
    def add(self, total_restarts = 0, cmd_xp_max = 15, cmd_xp_min = 15,
            msg_point_max = 2, msg_point_min = 2, msg_xp_max = 25,
            msg_xp_min = 15, cmd_point_max = 1, cmd_point_min = 1,
            level_base_xp = 2000, level_scaling_xp = 200, level_scaling_max = 40):

        add_bot = BotInfo(total_restarts, cmd_xp_max, cmd_xp_min,
                        msg_point_max, msg_point_min, msg_xp_max,
                        msg_xp_min, cmd_point_max, cmd_point_min,
                        level_base_xp, level_scaling_xp, level_scaling_max)

        Cache.botinfo = add_bot
        self.session.add(add_bot)

    def get(self):
        return Cache.botinfo
        for botinfo in Cache.botinfo:
            return botinfo

    def get_all(self):
        return self.session.query(BotInfo).all()

    def restarts_total(self):
        return

    def restarts_add(self):
        return

    def close(self):

        self.session.close()


class Command(DatabaseConntection):

    @Commit
    def add(self, server, author,
            command, response, alias = False,
            times_used = 0, deleted = False):

        add_command = Commands(server.id, author.id, command,
                               response, alias, times_used,
                               deleted)

        Cache.commands.append(add_command)
        self.session.add(add_command)
        return

    @Commit
    def remove(self, server, call):
        "Remove from database"
        self.session.query(Commands).filter(and_(Commands.command == call,
                                   Commands.server_id == server.id)).delete()

        for command in Cache.commands:
            if command.server_id == server.id and command.command == call:
                Cache.commands.remove(command)
                return
        return

    def delete(self, server, call):
        "Mark as deleted but save"
        return

    def get_all(self):
        return self.session.query(Commands).all()

    def exists(self, server, call):
        for command in Cache.commands:
            if command.server_id == server.id and command.command == call:
                return True
        return False

    def get(self, server, call):

        for command in Cache.commands:
            if command.server_id == server.id and command.command == call:
                return command
