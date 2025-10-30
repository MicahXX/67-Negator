import re

import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore messages from bots or pinned messages
    if message.author.bot or message.pinned:
        return

    # Check for "67" using regex
    if re.search(r'\b67\b', message.content):
        try:
            await message.delete()
        except discord.Forbidden:
            print("Missing permissions to delete messages.")
        except discord.HTTPException as e:
            print(f"Failed to delete message: {e}")

    await bot.process_commands(message)
    
    @BOT.event
async def on_message_edit(before, after):
    if after.author.bot or after.pinned:
        return

    if re.search(r'\b67\b', after.content):
        try:
            await after.delete()
        except discord.Forbidden:
            print("Missing permissions to delete an edited message.")
        except discord.NotFound:
            pass

# Bot Token
bot.run(os.getenv("TOKEN"))
