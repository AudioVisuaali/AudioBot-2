from sqlalchemy import (Column, String, Integer, Boolean,
                        ForeignKey, DateTime, text)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class BotInfo(Base):
    __tablename__ = "bot_info"

    id = Column(Integer, primary_key=True)
    total_restarts = Column(Integer, nullable=False, default=0)
    cmd_xp_max = Column(Integer, nullable=False, default=15)
    cmd_xp_min = Column(Integer, nullable=False, default=15)
    msg_point_max = Column(Integer, nullable=False, default=2)
    msg_point_min = Column(Integer, nullable=False, default=2)
    msg_xp_max = Column(Integer, nullable=False, default=25)
    msg_xp_min = Column(Integer, nullable=False, default=15)
    cmd_point_max = Column(Integer, nullable=False, default=1)
    cmd_point_min = Column(Integer, nullable=False, default=1)
    level_base_xp = Column(Integer, nullable=False, default=2000)
    level_scaling_xp = Column(Integer, nullable=False, default=200)
    level_scaling_max = Column(Integer, nullable=False, default=40)

    def __init__(self, total_restarts = 0, cmd_xp_max = 15,
                 cmd_xp_min = 15, msg_point_max = 2, msg_point_min = 2,
                 msg_xp_max = 25, msg_xp_min = 15, cmd_point_max = 1,
                 cmd_point_min = 1, level_base_xp = 2000, level_scaling_xp = 200,
                 level_scaling_max = 40):

        self.total_restarts = total_restarts
        self.cmd_xp_max = cmd_xp_max
        self.cmd_xp_min = cmd_xp_min
        self.msg_point_max = msg_point_max
        self.msg_point_min = msg_point_min
        self.msg_xp_max = msg_xp_max
        self.msg_xp_min = msg_xp_min
        self.cmd_point_max = cmd_point_max
        self.cmd_point_min = cmd_point_min
        self.level_base_xp = level_base_xp
        self.level_scaling_xp = level_scaling_xp
        self.level_scaling_max = level_scaling_max

class Servers(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True)
    server_id = Column(String(18), nullable=False)
    command_start = Column(String(32), nullable=False, default="!")
    tax_pot = Column(Integer, nullable=False, default=0)
    msg_point_max = Column(Integer, nullable=False, default=2)
    msg_point_min = Column(Integer, nullable=False, default=2)
    msg_xp_max = Column(Integer, nullable=False, default=25)
    msg_xp_min = Column(Integer, nullable=False, default=15)
    cmd_point_max = Column(Integer, nullable=False, default=1)
    cmd_point_min = Column(Integer, nullable=False, default=1)
    cmd_xp_max = Column(Integer, nullable=False, default=15)
    cmd_xp_min = Column(Integer, nullable=False, default=15)
    level_base_xp = Column(Integer, nullable=False, default=2000)
    level_scaling_xp = Column(Integer, nullable=False, default=200)
    level_scaling_max = Column(Integer, nullable=False, default=40)
    post_level = Column(Boolean, nullable=False, default=False)
    post_level_msg = Column(String(2000), nullable=False, default="{0} is now level {1}")
    post_level_same_channel_as_msg = Column(Boolean, nullable=False, default=False)
    post_info_channel = Column(String(18), default=None)
    casino_state = Column(Boolean, nullable=False, default=False)
    welcome_channel = Column(String(18), default=None)
    welcome_message = Column(String(2000), nullable=False, default="Welcome to the server {0}!")
    welcome_private = Column(Boolean, nullable=False, default=False)
    welcome_private_message = Column(String(2000), default=None)
    goodbye_channel = Column(String(18), default=None)
    goodbye_message = Column(String(2000), nullable=False, default="{3} left the server, hold those memories!")
    last_updated = Column(DateTime, nullable=False, default=text('NOW()'), onupdate=text('NOW()'))
    first_contact = Column(DateTime, nullable=False, server_default=text('NOW()'))

    def __init__(self, server_id, command_start="!",
                 tax_pot=0, msg_point_max=2, msg_point_min=2,
                 msg_xp_max=25, msg_xp_min=15, cmd_point_max=1,
                 cmd_point_min=1, cmd_xp_max=15, cmd_xp_min=15,
                 level_base_xp = 2000, level_scaling_xp = 200, level_scaling_max = 40,
                 post_level=False, post_level_msg= "{0} is now level {1}", post_level_same_channel_as_msg=False,
                 post_info_channel=None, casino_state=False, welcome_channel=None,
                 welcome_message="Welcome to the server {0}!", welcome_private=False, welcome_private_message=None,
                 goodbye_channel=None, goodbye_message="{3} left the server, hold those memories!"):

        self.server_id = server_id
        self.command_start = command_start
        self.tax_pot = tax_pot
        self.msg_point_max = msg_point_max
        self.msg_point_min = msg_point_min
        self.msg_xp_max = msg_xp_max
        self.msg_xp_min = msg_xp_min
        self.cmd_point_max = cmd_point_max
        self.cmd_point_min = cmd_point_min
        self.cmd_xp_max = cmd_xp_max
        self.cmd_xp_min = cmd_xp_min
        self.level_base_xp = level_base_xp
        self.level_scaling_xp = level_scaling_xp
        self.level_scaling_max = level_scaling_max
        self.post_level = post_level
        self.post_level_msg = post_level_msg
        self.post_level_same_channel_as_msg = post_level_same_channel_as_msg
        self.post_info_channel = post_info_channel
        self.casino_state = casino_state
        self.welcome_channel = welcome_channel
        self.welcome_message = welcome_message
        self.welcome_private = welcome_private
        self.welcome_private_message = welcome_private_message
        self.goodbye_channel = goodbye_channel
        self.goodbye_message = goodbye_message


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    d_id = Column(String(18), nullable=False)
    points = Column(Integer, nullable=False, default=0)
    bank = Column(Integer, nullable=False, default=0)
    xp = Column(Integer, nullable=False, default=0)
    level = Column(Integer, nullable=False, default=0)
    tokens = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime, nullable=False, default=text('NOW()'), onupdate=text('NOW()'))
    first_contact = Column(DateTime, nullable=False, server_default=text('NOW()'))

    def __init__(self, d_id, points=0, bank=0, xp=0, level=0, tokens=0):

        self.d_id = d_id
        self.points = points
        self.bank = bank
        self.xp = xp
        self.level = level
        self.tokens = tokens

class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    d_id = Column(String(18), nullable=False)
    server_id = Column(String(18), nullable=True)
    room_id = Column(String(18), nullable=False)
    message_id = Column(String(18), nullable=False)
    message_content = Column(String(2000), nullable=False)
    contains_images = Column(Boolean, nullable=False, default=False)
    private = Column(Boolean, nullable=False, default=False)
    deleted = Column(Boolean, nullable=False, default=False)
    last_updated = Column(DateTime, nullable=False, default=text('NOW()'), onupdate=text('NOW()'))
    first_contact = Column(DateTime, nullable=False, server_default=text('NOW()'))

    def __init__(self, d_id, server_id, room_id, message_id, message_content, private, contains_images=False, deleted=False):

        self.d_id = d_id
        self.server_id = server_id
        self.room_id = room_id
        self.message_id = message_id
        self.message_content = message_content
        self.contains_images = contains_images
        self.private = private
        self.deleted = deleted

class PointHistory(Base):
    __tablename__ = "point_history"

    id = Column(Integer, primary_key=True)
    d_id = Column(String(18), nullable=False)
    private = Column(Boolean, nullable=False, default=False)
    server_id = Column(String(18), nullable=True)
    mode_id = Column(Integer, nullable=False)
    mode_name = Column(String(18), nullable=False)
    stake_points = Column(String(18), nullable=True)
    stake_tokens = Column(String(18), nullable=True)
    outcome_points = Column(String(18), nullable=True)
    outcome_tokens = Column(String(18), nullable=True)
    info1 = Column(String(64), nullable=True)
    info2 = Column(String(64), nullable=True)
    info3 = Column(String(64), nullable=True)
    info4h = Column(String(64), nullable=True)
    info5h = Column(Integer, nullable=True, default=None)
    plus = Column(Integer, nullable=False, default=0)
    minus = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime, nullable=False, default=text('NOW()'), onupdate=text('NOW()'))
    first_contact = Column(DateTime, nullable=False, server_default=text('NOW()'))

    def __init__(self, d_id, server_id, mode_id,
                mode_name, private=False, stake_points=0, stake_tokens=0,
                outcome_points=0, outcome_tokens=0, info1=None,
                info2=None, info3=None, info4h=None,
                info5h=0, plus=0, minus=0):

        self.d_id = d_id
        self.private = private
        self.server_id = server_id
        self.mode_id = mode_id
        self.mode_name = mode_name
        self.stake_points = stake_points
        self.stake_tokens = stake_tokens
        self.outcome_points = outcome_points
        self.outcome_tokens = outcome_tokens
        self.info1 = info1
        self.info2 = info2
        self.info3 = info3
        self.info4h = info4h
        self.info5h = info5h
        self.plus = plus
        self.minus = minus

class Status(Base):
    __tablename__ = "users_status"

    id = Column(Integer, primary_key=True)
    d_id = Column(String(18), nullable=False)
    game_from = Column(String(256), nullable=True, default=None)
    game_to = Column(String(256), nullable=True, default=None)
    game_type = Column(Integer, nullable=False, default=0)
    status_from = Column(String(16), nullable=False)
    status_to = Column(String(16), nullable=False)
    last_updated = Column(DateTime, nullable=False, default=text('NOW()'), onupdate=text('NOW()'))
    first_contact = Column(DateTime, nullable=False, server_default=text('NOW()'))

    def __init__(self, d_id, game_from, game_to,
                 game_type, status_from, status_to):

        self.d_id = d_id
        self.game_from = game_from
        self.game_to = game_to
        self.game_type = game_type
        self.status_from = status_from
        self.status_to = status_to

class Nicknames(Base):
    __tablename__ = "users_nicknames"

    id = Column(Integer, primary_key=True)
    d_id = Column(String(18), nullable=False)
    nickname = Column(String(32), nullable=False)
    last_updated = Column(DateTime, nullable=False, default=text('NOW()'), onupdate=text('NOW()'))
    first_contact = Column(DateTime, nullable=False, server_default=text('NOW()'))

    def __init__(self, d_id, nickname):

        self.d_id = d_id
        self.nickname = nickname

class Commands(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True)
    server_id = Column(String(18), nullable=False)
    adder_id = Column(String(18), nullable=False)
    command = Column(String(64), nullable=False)
    response = Column(String(2000), nullable=False)
    alias = Column(Boolean, nullable=False, default=False)
    times_used = Column(Integer, nullable=False, default=0)
    deleted = Column(Boolean, nullable=False, default=False)
    last_updated = Column(DateTime, nullable=False, default=text('NOW()'), onupdate=text('NOW()'))
    first_contact = Column(DateTime, nullable=False, server_default=text('NOW()'))

    def __init__(self, server_id, adder_id, command,
                 response, alias, times_used, deleted=False):

        self.server_id = server_id
        self.adder_id = adder_id
        self.command = command
        self.response = response
        self.alias = alias
        self.times_used = times_used
        self.deleted = deleted
