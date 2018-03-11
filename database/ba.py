import config
from pymysql import connect as pconnect

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Database:

    def __init__(self):

        # Connector
        self.server = Server()
        self.logs = Logging_database()
        self.bot = Bot_info()
        self.message = Message()
        Database_connection.__init__(self)


class Database_connection(Flask):

    def __init__(self):

        self.config[] =
        
        self.db = SQLAlchemy(self)


        self.engine = create_engine("sqlite:///census_nyc.sqlite")

        self.connection = self.engine.connect()

        print(self.)



    def logging_message_add_to_db(self, aaa):
        self.cur.execute("INSERT INTO d_id, server_id, room_id, message_id, private, message, deleted VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", ())
        self.conn.commit()
        return

asd = """class Database_connection:

    def __init__(self):

        # login
        self.db_name = config.db_name
        self.db_pwd = config.db_password
        self.db_usr = config.db_username
        self.db_host = config.db_host
        self.db_port = config.db_port
        self.db_charset = "utf8mb4"

        # Connector
        self.conn = pconnect(host=self.db_host, user=self.db_usr, passwd=self.db_pwd, db=self.db_name, charset=self.db_charset,)
        self.cur = self.conn.cursor()

        # Adding restart
        #self.cur.execute("UPDATE server_stats SET restarts = restarts + 1;")
        #self.conn.commit()


    def logging_message_add_to_db(self, aaa):
        self.cur.execute("INSERT INTO d_id, server_id, room_id, message_id, private, message, deleted VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", ())
        self.conn.commit()
        return"""


class Server(Database_connection):

    def check(self):
        "Return the servers in database to be compared"

        # Query
        self.cur.execute("SELECT server_id FROM servers;")

        # Commit
        self.conn.commit()

        # Fetfch
        return self.cur.fetchall()

    def new(self, server_id):
        "Create a server in the database"

        # Query
        self.cur.execute("INSER INTO servers (server_id) VALUES (%s)", (server_id,))

        # Commit
        self.conn.commit()
        return

class Logging_database(Database_connection):

    def __init__(self):
        #database = Database()
        return

    def add_message(self, message):

        # ADD logging to cmd and logging system

        info = []
        private = 0
        deleted = 0
        id_server = ""
        name = str(message.author)
        id_message = str(message.id)
        content = str(message.content)
        id_user = str(message.author.id)
        id_channel = str(message.channel.id)
        image = str(str(message.attachments)[1:-1]).replace("'", '"')


    # Checks if messages are sent in the last x // author id, seconds
    # Returns true or false
    def is_messages_sent(self, d_id, seconds):
        print("43564534563645645")
        return


class Bot_info(Database_connection):

    def __init__(self):
        return

class Message(Database_connection):

    def check_user_and_server():
        "Checks if server and user exists in the database"

        # Query
        self.cur.execute("SELECT server_id FROM servers;")

        # Commit
        self.conn.commit()

        # Fetfch
        return self.cur.fetchall()
