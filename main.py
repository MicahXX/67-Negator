import asyncio
import os
from bot import bot, load_extensions

async def main():
    await load_extensions()
    await bot.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())