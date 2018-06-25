from main import Bot

import logging, sys

# Setup logging
#log_level = getattr(logging, )
#log_format = config.LOG_FORMAT

# Logger
#logger = logging.getLogger('audiobot')
#logger.setLevel(log_level)

# Format
#log_formatter = logging.Formatter(log_format)

#log_console_handle = logging.StreamHandler()
#log_console_handle.setLevel(log_level)
#log_console_handle.setFormatter(log_formatter)
#logger.addHandler(log_console_handle)

#if config.LOG_FILE_PATH:
#    log_file_handle = logging.FileHandler()
#    log_file_handle.setLevel(log_level)
#    log_file_handle.setFormatter(log_formatter)
#    logger.addHandler(log_file_handle)


def main():
    DiscordBot = Bot()
    DiscordBot.start_bot()


if __name__ == "__main__":
    main()
