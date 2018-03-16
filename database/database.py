from sqlalchemy import (Table, Column, Integer,
                        Date, select, literal, and_,
                        exists, create_engine, update,
                        func, desc)
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.sql import exists, and_
from utils.decorators import Commit, IsBoolean, IsInteger, IsString
from database.tables import (Servers, Users, Messages,
                             PointHistory, Commands, BotInfo,
                             DailyRedeem, Nicknames, Doubles,
                             Status, Base)
from datetime import datetime, timedelta
from utils import Utils
import time

# Database connector
class Database:

    def __init__(self):

        self.config = None
        self.addr = None
        self.engine = None
        self.session = None

    def connect(self):

        # Utils / config
        util = Utils()
        self.config = util.get_config_info()

        # creating engine
        self.addr = '{0.type}://{0.username}:{0.password}@{0.address}/{0.database}'.format(self.config.database)

        self.engine = create_engine(self.addr, echo=False, convert_unicode=True)

        # Creating tables
        Base.metadata.create_all(self.engine)

        # Session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # mapping
        self.user = User(self.session)
        self.server = Server(self.session)
        self.message = Message(self.session)
        self.pointhistory = Points(self.session)
        self.bot = Bot(self.session)
        self.command = Command(self.session)
        self.cache = Cache(self.session)
        self.redeem = Redeem(self.session)
        self.nickname= Nickname(self.session)
        self.double = Double(self.session)
        self.status = UserStatus(self.session)

        # Creating cache
        Cache.get_cache(self)

    def close(self):

        self.session.close()

    def dispose(self):

        self.engine.dispose()

class UserStatus:

    def __init__(self, session):
        self.session = session

    @Commit
    def add(self, d_id, game_from, game_to, game_type, status_from, status_to):

        add_double = Status(d_id, game_from, game_to, game_type,
                             status_from, status_to)

        self.session.add(add_double)
        return

class Cache:

    def __init__(self, session):
        self.session = session

    users = []
    servers = []
    commands = []
    module_timeouts = []
    nicknames = []
    botinfo = None

    def get_cache(self):

        for server in Server.get_all(self):
            Cache.servers.append(server)

        for user in User.get_all(self):
            Cache.users.append(user)

        for command in Command.get_all(self):
            Cache.commands.append(command)

        for nickname in Nickname.get_all(self):
            Cache.nicknames.append(nickname)

        botstats = Bot.get_all(self)
        if not botstats:
            Bot.add(self, total_restarts = 0, cmd_xp_max = 15, cmd_xp_min = 15, msg_xp_max = 25, msg_xp_min = 15)
        else:
            Cache.botinfo = botstats[0]

        Bot.restarts_add(self)
        return

    def reload_cache(self):
        calc = 0
        _users = []
        _servers = []
        _commands = []
        _module_timeouts = []
        _nicknames = []
        _botinfo = None

        for server in Server.get_all(self):
            calc += 1
            _servers.append(server)

        for user in User.get_all(self):
            calc += 1
            _users.append(user)

        for command in Command.get_all(self):
            calc += 1
            _commands.append(command)

        for nickname in Nickname.get_all(self):
            calc += 1
            _nicknames.append(nickname)

        botstats = Bot.get_all(self)
        if not botstats:
            Bot.add(self, total_restarts = 0, cmd_xp_max = 15, cmd_xp_min = 15, msg_xp_max = 25, msg_xp_min = 15)
        else:
            _botinfo = botstats[0]
        calc += 1

        Cache.servers = _servers
        Cache.users = _users
        Cache.commands = _commands
        Cache.nicknames = _nicknames
        Cache.botinfo = _botinfo

        return calc


class Double:

    def __init__(self, session):
        self.session = session

    @Commit
    def add(self, d_id, number1, number2, is_double,
            victory_memes, victory_tokens):

        add_double = Doubles(d_id, number1, number2, is_double,
                             victory_memes, victory_tokens)

        self.session.add(add_double)
        return

    def get_stats_user(self, d_id):

        asd = self.session.query(func.count(Doubles.d_id).\
                                    filter(Doubles.d_id == d_id),
                                 func.count(Doubles.d_id).\
                                    filter(and_(Doubles.is_double == True,
                                                Doubles.d_id == d_id)),
                                 func.sum(Doubles.victory_memes).\
                                    filter(Doubles.d_id == d_id),
                                 func.sum(Doubles.victory_tokens).\
                                    filter(Doubles.d_id == d_id)).\
                                 all()[0]

        class Fdg:
            def __init__(self, rows, doubles, memes, tokens):
                self.rows = rows
                self.doubles = doubles
                self.memes = memes
                self.tokens = tokens

        return Fdg(asd[0],asd[1],asd[2],asd[3])

# User
class User:

    def __init__(self, session):
        self.session = session

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

        self.session.execute(stmt)

        return

    @IsInteger
    def bank_alter(self, d_id, point_amount):

        for user in Cache.users:
            if user.d_id == d_id:
                user.bank += point_amount

        stmt = update(Users).where(Users.d_id == d_id).\
                values(bank = Users.bank + point_amount)

        self.session.execute(stmt)

        return

    @IsInteger
    def xp_alter(self, d_id, xp_amount):

        for user in Cache.users:
            if user.d_id == d_id:
                user.xp += xp_amount

        stmt = update(Users).where(Users.d_id == d_id).\
                values(xp = Users.xp + xp_amount)

        self.session.execute(stmt)

        return

    @IsInteger
    def level_alter(self, d_id, level_amount):

        for user in Cache.users:
            if user.d_id == d_id:
                user.level += level_amount

        stmt = update(Users).where(Users.d_id == d_id).\
                values(level = Users.level + level_amount)

        self.session.execute(stmt)

        return

    @IsInteger
    def level_set(self, d_id, level_set):

        for user in Cache.users:
            if user.d_id == d_id:
                user.level = level_set

        stmt = update(Users).where(Users.d_id == d_id).\
                values(level = level_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def tokens_alter(self, d_id, tokens_amount):

        for user in Cache.users:
            if user.d_id == d_id:
                user.tokens += tokens_amount

        stmt = update(Users).where(Users.d_id == d_id).\
                values(tokens = Users.tokens + tokens_amount)

        self.session.execute(stmt)

        return

# Server
class Server:

    def __init__(self, session):
        self.session = session

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

        self.session.execute(stmt)

        return

    @IsInteger
    def tax_pot_alter(self, server_id, tax_pot_alter):

        for server in Cache.servers:
            if server.server_id == server_id:
                server.tax_pot += tax_pot_alter

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(tax_pot = Servers.tax_pot + tax_pot_alter)
        self.session.execute(stmt)

        return

    @IsInteger
    def msg_point_max_set(self, server_id, point_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.msg_point_max = point_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(msg_point_max = point_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def msg_point_min_set(self, server_id, point_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.msg_point_min = point_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(msg_point_min = point_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def msg_xp_max_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.msg_xp_max = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(msg_xp_max = xp_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def msg_xp_min_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.msg_xp_min = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(msg_xp_min = xp_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def cmd_point_max_set(self, server_id, point_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.cmd_point_max = point_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(cmd_point_max = point_set)

        self.session.execute(stmt)

    @IsInteger
    def cmd_point_min_set(self, server_id, point_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.cmd_point_min = point_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(cmd_point_min = point_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def cmd_xp_max_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.cmd_xp_max = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(cmd_xp_max = xp_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def cmd_xp_min_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.cmd_xp_min = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(cmd_xp_min = xp_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def level_base_xp_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.level_base_xp = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(level_base_xp = xp_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def level_scaling_xp_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.level_scaling_xp = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(level_scaling_xp = xp_set)

        self.session.execute(stmt)

        return

    @IsInteger
    def level_scaling_max_set(self, server_id, xp_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.level_scaling_max = xp_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(level_scaling_max = xp_set)

        self.session.execute(stmt)

        return

    @IsBoolean
    def post_level_set(self, server_id, boolean_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.post_level = boolean_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(post_level = boolean_set)

        self.session.execute(stmt)

        return

    @IsString
    def post_level_msg_set(self, server_id, level_msg):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.post_level_msg = level_msg

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(post_level_msg = level_msg)

        self.session.execute(stmt)

        return

    @IsBoolean
    def post_level_same_channel_as_msg_set(self, server_id, boolean_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.post_level_same_channel_as_msg = boolean_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(post_level_same_channel_as_msg = boolean_set)

        self.session.execute(stmt)

        return

    @IsString
    def post_info_channel_set(self, server_id, channel_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.post_info_channel = channel_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(post_info_channel = channel_set)

        self.session.execute(stmt)

        return

    @IsBoolean
    def casino_state_set(self, server_id, state_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.casino_state = state_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(casino_state = state_set)

        self.session.execute(stmt)

        return

    @IsString
    def welcome_channel_set(self, server_id, channel_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.welcome_channel = channel_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(welcome_channel = channel_set)

        self.session.execute(stmt)

        return

    @IsString
    def welcome_message_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.welcome_message = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(welcome_message = message_set)

        self.session.execute(stmt)

        return

    @IsBoolean
    def welcome_private_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.welcome_private = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(welcome_private = message_set)

        self.session.execute(stmt)

        return

    @IsString
    def welcome_private_message_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.welcome_private_message = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(welcome_private_message = message_set)

        self.session.execute(stmt)

        return

    @IsString
    def goodbye_channel_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.goodbye_channel = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(goodbye_channel = message_set)

        self.session.execute(stmt)

        return

    @IsString
    def goodbye_message_set(self, server_id, message_set):

        # TODO add limit somehow
        for server in Cache.servers:
            if server.server_id == server_id:
                server.goodbye_message = message_set

        stmt = update(Servers).where(Servers.server_id == server_id).\
                values(goodbye_message = message_set)

        self.session.execute(stmt)

        return

class Message:

    def __init__(self, session):
        self.session = session

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

        self.session.execute(stmt)

        return

class Points:

    def __init__(self, session):
        self.session = session

    @Commit
    def add(self, d_id, server_id, mode_id,
            mode_name, private=False, stake_points=0, stake_tokens=0,
            outcome_points=0, outcome_tokens=0, info1="",
            info2="", info3="", info4h="",
            info5h=0, plus=0, minus=0):

        pointsadd = PointHistory(d_id, server_id, mode_id,
                    mode_name, private, stake_points, stake_tokens,
                    outcome_points, outcome_tokens, info1,
                    info2, info3, info4h,
                    info5h, plus, minus)

        self.session.add(pointsadd)

        return

    def get_min_bank_amount(mode, interval, d_id):

        current_time = datetime.utcnow()

        time_ago = current_time - timedelta(seconds=interval)

        response = self.session.query(func.min(PointHistory.info5h).label("min_bank")).\
                        filter(and_(PointHistory.first_contact > time_ago,
                                PointHistory.d_id == d_id,
                                PointHistory.mode_id == mode))

        return response

    def get_history_user(self, d_id, total = 10):

        response = self.session.query(PointHistory).filter(PointHistory.d_id == d_id).order_by(desc(PointHistory.first_contact)).limit(total).all()

        return response

class Bot:

    def __init__(self, session):
        self.session = session

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

        stmt = update(BotInfo).values(total_restarts = BotInfo.total_restarts + 1)

        self.session.execute(stmt)
        Cache.botinfo.total_restarts += 1
        return

    def close(self):

        self.session.close()

class Redeem:

    def __init__(self, session):
        self.session = session

    @Commit
    def add(self, d_id, day, amount):

        add_command = DailyRedeem(d_id, day, amount)

        self.session.add(add_command)
        return

    def check_daily(self, d_id, day):

        return self.session.query(DailyRedeem).filter(and_(DailyRedeem.d_id == d_id,
                                           DailyRedeem.day == day)).all()
        return response

class Command:

    def __init__(self, session):
        self.session = session

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

    def get_all_server(self, server_id):

        command_list = []

        for command in Cache.commands:
            if command.server_id == server_id:
                command_list.append(command)

        return command_list

class Nickname:

    def __init__(self, session):
        self.session = session

    @Commit
    def add(self, d_id, nickname_before, nickname_after):

        add_nick = Nicknames(d_id, nickname_before, nickname_after)

        Cache.commands.append(add_nick)
        self.session.add(add_nick)
        return

    def get_all(self):
        return self.session.query(Nicknames).all()

    def get_user_nicks(self, d_id):

        nick_list = []

        for nickname in Cache.nicknames:
            if nickname.d_id == d_id:
                nick_list.append(nickname)

        return nick_list
