from newdb import Database

database = Database()


def add_data():
    database.user.add(127480853742747648)
    database.server.add(279619091055116291)
    database.message.add(127480853742747648, 279619091055116291, 381889648827301889, 414313733788270592, "adfsfsadfsadsfadfsfsd", False, False, False)
    database.points.add(d_id=127480853742747648, server_id=279619091055116291, mode_id=10, mode_name="Bandk")
    database.user.add(127480853742747648)
    database.server.add(279619091055116291)
    database.message.add(127480853742747648, 279619091055116291, 381889648827301889, 414313733788270592, "adfsfsadfsadsfadfsfsd", False, False, False)
    database.points.add(d_id=127480853742747648, server_id=279619091055116291, mode_id=10, mode_name="Bandk")
    database.user.add(127480853742747648)
    database.server.add(279619091055116291)
    database.message.add(127480853742747648, 279619091055116291, 381889648827301889, 414313733788270592, "adfsfsadfsadsfadfsfsd", False, False, False)
    database.points.add(d_id=127480853742747648, server_id=279619091055116291, mode_id=10, mode_name="Bandk")

#add_data()
ccc = database.server.get_all()
for cc in ccc:
    print(cc.server_id, cc.command_start)


aaa = database.server.exists("279619091055116291")

print(aaa)
