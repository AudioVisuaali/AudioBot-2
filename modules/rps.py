import random

# RPS BY WOLFIE <3
class Rps:

    async def main(self, bot, database, message, arguments):

        #USERINPUT
        userinput = arguments[0]

        #OPTIONS
        options = ["rock", "paper", "scissors"]
        random_number = random.randint(0,2)

        #COMPUTER INPUT
        botinput = options[random_number]

        #VALIDATION
        if not (userinput.lower() in options):
            send_message = "That isn't right!"
            await bot.say(message.channel, "<@"+message.author.id+"> "+send_message)
            return

        #ANSWER - Draw
        if botinput == userinput:
            send_message = "Draw"

        #ANSWER - Rock
        elif botinput == "rock":
            if userinput == "paper":
                send_messagesend_message = "Paper beats Rock, you win!"
            else:
                send_message = "You lose!"

        #ANSWER - Paper
        elif botinput == "paper":
            if userinput == "scissors":
                send_message = "Scissors beats paper, you win!"
            else:
                send_message = "You lose!"

        #ANSWER - Scissors
        elif botinput == "scissors":
            if userinput == "rock":
                send_message = "Rock beats Scissors, you win!"
            else:
                send_message = "You lose!"

        await bot.say(message.channel, "<@"+message.author.id+"> "+send_message)
