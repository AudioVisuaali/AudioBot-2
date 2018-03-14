from main import Bot

#import logging, sys

# logging
#LOG_FILENAME = 'bot.log'
#logging.basicConfig(filename=LOG_FILENAME, level=logging.WARNING)

def main():
    DiscordBot = Bot()
    DiscordBot.start_bot()

if __name__ == "__main__":
    main()
