import aiohttp
import asyncio

class Web:

    async def get_content(self, address):
        async with aiohttp.ClientSession() as session:
            async with session.get(address.replace(" ", "_")) as resp:
                if resp.status != 200:
                    return

                return await resp.text()
