import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    for ext in [
        "events.on_ready",
        "events.on_message",
        "events.on_message_edit",
        "events.on_reaction",
        "commands.exclusions",
    ]:
        await bot.load_extension(ext)
