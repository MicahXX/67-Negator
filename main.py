import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

EXEMPT_USER_ID = 701156951798841364  # replace with your own user ID

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Function to check for banned patterns
def contains_banned_pattern(content: str) -> bool:
    lowered = content.lower()

    # Common separators
    separators = [" ", "-", "_", "/", "&", ".", "~", ","]

    # Normalize text by removing separators
    normalized = lowered
    for sep in separators:
        normalized = normalized.replace(sep, "")

    # Patterns that should trigger deletion (with or without separators)
    banned_combos = [
        "67",
        "sixseven",
    ]

    # Direct match with no operator
    if any(pattern in normalized for pattern in banned_combos):
        return True

    # Match with separators
    for sep in separators:
        if f"6{sep}7" in lowered or f"six{sep}seven" in lowered:
            return True

    return False

# Check new messages
@bot.event
async def on_message(message):
    if message.author.bot or message.pinned:
        return
    if message.author.id == EXEMPT_USER_ID:
        return

    if contains_banned_pattern(message.content):
        try:
            await message.delete()
        except discord.Forbidden:
            print("Missing permissions to delete messages.")
        except discord.HTTPException as e:
            print(f"Failed to delete message: {e}")

    await bot.process_commands(message)

# Check edited messages
@bot.event
async def on_message_edit(before, after):
    if after.author.bot or after.pinned:
        return
    if after.author.id == EXEMPT_USER_ID:
        return

    if contains_banned_pattern(after.content):
        try:
            await after.delete()
            print(f"Deleted edited message from {after.author}: {after.content}")
        except discord.Forbidden:
            print("Missing permissions to delete edited messages.")
        except discord.NotFound:
            pass

# Bot Token
bot.run(os.getenv("TOKEN"))