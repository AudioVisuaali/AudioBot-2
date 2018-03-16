import aiohttp
import asyncio

class Web:

    async def get_content(self, address):
        async with aiohttp.ClientSession() as session:
            async with session.get(address.replace(" ", "_")) as resp:
                if resp.status != 200:
                    return

                return await resp.text()

    async def get_image(self, address, bot):
        with aiohttp.Timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(address) as res:
                    await bot.edit_profile(avatar=await res.read())
                    #return res
