from asyncio import sleep as asleep
from random import randint
from math import floor

class SlotMachine:

    # Getting fruits and values
    def fruit_multiplier(self, fruit = None):

        # these are direction giving there not calculated
        # these values are get by brute force
        fruits = {
                 ":honey_pot:": float("10"),
                 ":eggplant:": float("7.5"),
                 ":banana:": float("6.5"),
                 ":peach:": float("5.5"),
                 ":cherries:": float("4.5"),
                 ":apple:": float("3.5")
             }

        # Returning fruits list
        if fruit is None:
            return fruits.keys()

        # Returning value
        else:
             return fruits[fruit]

    # Createing inside
    def create_slots_frame(self, message, value):

            # This case honeypot, xxxx, green_apple
            header1 = ":slot_machine: **| You rolled the slot machine!!\n\n===== SLOTS =====**\n"
            kappa = [["","",""],["","",""],["","",""]]

            # Generating each column
            for i in range(3):
                r = randint(0,5)
                fruits = [fruit_name for fruit_name in self.fruit_multiplier()]

                # generating each row in column
                for u in range(3):
                    r = randint(0, len(fruits)-1)
                    kappa[i-1][u-1] = fruits[r]
                    fruits.pop(r)

                    # Handle
            for p in range(3):
                if p == 0:
                    sss = "      :red_circle:"
                elif p == 1:
                    sss = ":french_bread:"
                else:
                    sss = ""
                header1 += "[{}] - [{}] - [{}] {}\n".format(kappa[0][p], kappa[1][p], kappa[2][p], sss)

            # Don't @ me
            if value == 0:
                header1 += "\n<@{}>".format(message.author.id)
            else:
                header1 += ""

            return kappa, header1

    # Slots
    async def main(self, bot, database, message, arguments):

            users_points = bot.database.user.get(message.author.id).points
            if len(arguments) == 0:
                await bot.say(message.channel, ":slot_machine: **| You need to gamble atleast 10 memes!**")
                return

            # if not all run through letter check 1k = 1000
            if arguments[0] != "all":

                # Checking for k=1000 points
                if "k" in arguments[0]:
                    arguments[0] = float(arguments[0].lower().replace("k","")) * 1000

                #Checking if number
                try:
                    arguments[0] = int(arguments[0])
                except ValueError:
                    send(1, "Invalid currency or amount")
                    return

            # if all set pot amount to users max points
            else:
                arguments[0] = users_points

            # checking if user has enough points to gamble
            if users_points < int(arguments[0]):
                await bot.say(message.channel, ":slot_machine: **| You don't have enough points to gamble!**")
                return

            # Gambled more than 10 memes?
            if int(arguments[0]) < 10:
                await bot.say(message.channel, ":slot_machine: **| You need to gamble atleast 10 memes!**")
                return

            # if user has more points than 10?
            if users_points < 10:
                await bot.say(message.channel, ":slot_machine: **| You need to gamble atleast 10 memes!**")
                return

            # message state 1
            header1_stuff = self.create_slots_frame(message, 0)
            header1 = header1_stuff[1]

            # Message state 2
            header2_stuff = self.create_slots_frame(message, 0)
            header2 = header2_stuff[1]

            # Message state Final
            header_og = self.create_slots_frame(message, 1)
            kappa = header_og[0]
            header = header_og[1] + "\n"

            # values
            multiplier = 0.0
            straights = 0
            emojis = []

            """        # O O O
            # O O X
            # X X O
            if kappa[0][2] == kappa[1][2] == kappa[2][1]:
                straights += 1
                item = kappa[0][2]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O O X
            # X X O
            # O O O
            if kappa[0][1] == kappa[1][1] == kappa[2][0]:
                straights += 1
                item = kappa[0][1]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O O O
            # X O O
            # O X X
            if kappa[0][1] == kappa[1][2] == kappa[2][2]:
                straights += 1
                item = kappa[0][1]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # X O O
            # O X X
            # O O O
            if kappa[0][0] == kappa[1][1] == kappa[2][1]:
                straights += 1
                item = kappa[0][0]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # X X O
            # O O X
            # O O O
            if kappa[0][0] == kappa[1][0] == kappa[2][1]:
                straights += 1
                item = kappa[0][0]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O O O
            # X X O
            # O O X
            if kappa[0][1] == kappa[1][1] == kappa[2][2]:
                straights += 1
                item = kappa[0][1]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O O O
            # O X X
            # X O O
            if kappa[0][2] == kappa[1][1] == kappa[2][1]:
                straights += 1
                item = kappa[0][2]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O X X
            # X O O
            # O O O
            if kappa[0][1] == kappa[1][0] == kappa[2][0]:
                straights += 1
                item = kappa[0][1]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O X O
            # X O X
            # O O O
            if kappa[0][1] == kappa[1][0] == kappa[2][1]:
                straights += 1
                item = kappa[0][1]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O O O
            # O X O
            # X O X
            if kappa[0][2] == kappa[1][1] == kappa[2][2]:
                straights += 1
                item = kappa[0][2]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O O O
            # X O X
            # O X O
            if kappa[0][1] == kappa[1][2] == kappa[2][1]:
                straights += 1
                item = kappa[0][1]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # X O X
            # O X O
            # O O O
            if kappa[0][0] == kappa[1][1] == kappa[2][0]:
                straights += 1
                item = kappa[0][0]
                multiplier += floor(self.fruit_multiplier(item)*0.2)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)"""


            # X X X
            # O O O
            # O O O
            if kappa[0][0] == kappa[1][0] == kappa[2][0]:
                straights += 1
                item = kappa[0][0]
                multiplier += self.fruit_multiplier(item)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O O O
            # X X X
            # O O O
            if kappa[0][1] == kappa[1][1] == kappa[2][1]:
                straights += 1
                item = kappa[0][1]
                multiplier += self.fruit_multiplier(item)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O O O
            # O O O
            # X X X
            if kappa[0][2] == kappa[1][2] == kappa[2][2]:
                straights += 1
                item = kappa[0][2]
                multiplier += self.fruit_multiplier(item)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # X O O
            # O X O
            # O O X
            if kappa[0][0] == kappa[1][1] == kappa[2][2]:
                straights += 1
                item = kappa[0][0]
                multiplier += self.fruit_multiplier(item)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # O O X
            # O X O
            # X O O
            if kappa[0][2] == kappa[1][1] == kappa[2][0]:
                straights += 1
                item = kappa[2][0]
                multiplier += self.fruit_multiplier(item)
                header += "You've got a {} streak\n".format(item)
                emojis.append(item)

            # Multiplier for 2 straights
            if straights == 2:
                multiplier += 5.0
            elif straights == 3:
                multiplier += 15.0

            # Multiplier
            if multiplier == 0.0:
                win_amount = arguments[0]
                win_str_plus = "-" + str(win_amount)
                minus = int(win_amount)
                plus = 0
            else:
                win_amount = floor(int(arguments[0])*multiplier)
                if straights > 0:
                    win_str_plus = "+" + str(win_amount-int(arguments[0]))
                    minus = 0
                    plus = win_amount-int(arguments[0])

            # gamble logging
            try:
                info1 = emojis[0]
            except:
                info1 = ""

            # gamble logging
            try:
                info2 = emojis[1]
            except:
                info2 = ""

            # gamble logging
            try:
                info3 = emojis[2]
            except:
                info3 = ""

            # Creating message
            if straights > 0:
                header += "\n:white_check_mark: **| <@{}>, you have won {} memes, you now have {} memes!**".format(message.author.id, str(win_amount), str(int(users_points)+int(win_amount)))
                bot.database.user.points_alter(message.author.id, win_amount)
            else:
                header += "\n:x: **| <@{}>, you have lost {} memes, you now have {} memes!**".format(message.author.id, str(win_amount), str(int(users_points)-int(win_amount)))
                bot.database.user.points_alter(message.author.id, -win_amount)

            # gamble logging adding
            bot.database.pointhistory.add(message.server.id, message.author.id, 8, "Slots", False, arguments[0], "", win_str_plus, "", info1, info2, info3, "", 0, plus, minus)
            # Send state 1
            sent = await bot.say(message.channel, header1)

            # Send state 2
            await asleep(.5)
            await bot.edit_message(sent, header2)

            # send state Final
            await asleep(.5)
            await bot.edit_message(sent, header)
