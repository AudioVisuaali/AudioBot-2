from discord import Game

class Playing:

    async def main(self, bot, database, message, arguments):
        
        await bot.change_presence(game=Game(name=arguments[0]))
