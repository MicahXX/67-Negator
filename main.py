import discord
import os
import re
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

EXEMPT_USER_ID = 701156951798841364  # exempt User
EXCLUDED_CHANNEL_IDS = {1406903279278886952}  # exempt Channel


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# Regex to match actual Discord emojis
CUSTOM_EMOJI_PATTERN = re.compile(r"^<a?:\w+:\d+>$")

# Regex to match Unicode emojis
UNICODE_EMOJI_PATTERN = re.compile(
    r"^[\U0001F1E0-\U0001FAFF\u2600-\u26FF\u2700-\u27BF\uFE0F\u200D\s]+$"
)


def is_emoji_only_message(text: str) -> bool:
    text = text.strip()
    if not text:
        return False

    # Split into parts (to allow multiple emojis)
    parts = text.split()
    return all(
        CUSTOM_EMOJI_PATTERN.fullmatch(part) or UNICODE_EMOJI_PATTERN.fullmatch(part)
        for part in parts
    )


def contains_banned_pattern(content: str) -> bool:
    lowered = content.lower().strip()

    # Ignore emoji only messages (custom or Unicode)
    if is_emoji_only_message(lowered):
        return False

    # Exclude links and mentions
    if "http://" in lowered or "https://" in lowered:
        return False
    if "@" in lowered:
        return False

    # Normalize for pattern detection
    separators = [" ", "-", "_", "/", "&", ".", "~", ","]

    normalized = lowered
    for sep in separators:
        normalized = normalized.replace(sep, "")

    # Banned patterns
    banned_combos = ["67", "sixseven", "sixtyseven"]

    if any(pattern in normalized for pattern in banned_combos):
        return True

    for sep in separators:
        if f"6{sep}7" in lowered or f"six{sep}seven" in lowered:
            return True

    return False


@bot.event
async def on_message(message):
    if message.author.bot or message.pinned:
        return
    if message.author.id == EXEMPT_USER_ID:
        return
    if message.channel.id in EXCLUDED_CHANNEL_IDS:
        return

    if contains_banned_pattern(message.content):
        try:
            await message.delete()
        except discord.Forbidden:
            print("Missing permissions to delete messages.")
        except discord.HTTPException as e:
            print(f"Failed to delete message: {e}")

    await bot.process_commands(message)


@bot.event
async def on_message_edit(before, after):
    if after.author.bot or after.pinned:
        return
    if after.author.id == EXEMPT_USER_ID:
        return
    if after.channel.id in EXCLUDED_CHANNEL_IDS:
        return

    if contains_banned_pattern(after.content):
        try:
            await after.delete()
        except discord.Forbidden:
            print("Missing permissions to delete edited messages.")
        except discord.NotFound:
            pass


bot.run(os.getenv("TOKEN"))