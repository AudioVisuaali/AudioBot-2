class Purge:

    async def main(self, bot, database, message, arguments):

        kek = bot.database.cache.reload_cache()
        lul = bot.timeout.delete_timeouts()
        
        await bot.say(message.channel, "Reloaded {} and deleted {}".format(kek, lul))
