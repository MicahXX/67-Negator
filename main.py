import discord
import os
import re
import json
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
EXCLUSIONS_FILE = "exclusions.json"

def load_exclusions():
    if not os.path.exists(EXCLUSIONS_FILE):
        return {}
    with open(EXCLUSIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_exclusions():
    with open(EXCLUSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(exclusions, f, indent=4)

def get_guild_data(guild_id: int):
    guild_id = str(guild_id)
    if guild_id not in exclusions:
        exclusions[guild_id] = {"users": [], "channels": []}
    return exclusions[guild_id]

exclusions = load_exclusions()

CUSTOM_EMOJI_PATTERN = re.compile(r"^<a?:\w+:\d+>$")
UNICODE_EMOJI_PATTERN = re.compile(
    r"^[\U0001F1E0-\U0001FAFF\u2600-\u26FF\u2700-\u27BF\uFE0F\u200D\s]+$"
)

def is_emoji_only_message(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    parts = text.split()
    return all(
        CUSTOM_EMOJI_PATTERN.fullmatch(part) or UNICODE_EMOJI_PATTERN.fullmatch(part)
        for part in parts
    )

def contains_banned_pattern(content: str) -> bool:
    lowered = content.lower().strip()
    if is_emoji_only_message(lowered):
        return False
    if "http://" in lowered or "https://" in lowered:
        return False
    if "@" in lowered:
        return False
    separators = [" ", "-", "_", "/", "&", ".", "~", ","]
    normalized = lowered
    for sep in separators:
        normalized = normalized.replace(sep, "")
    banned_combos = ["67", "sixseven", "sixtyseven"]
    if any(pattern in normalized for pattern in banned_combos):
        return True
    for sep in separators:
        if f"6{sep}7" in lowered or f"six{sep}seven" in lowered:
            return True
    return False

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} — Slash commands synced.")

@bot.event
async def on_message(message):
    if message.author.bot or message.pinned or not message.guild:
        return
    guild_data = get_guild_data(message.guild.id)
    if message.author.id in guild_data["users"]:
        return
    if message.channel.id in guild_data["channels"]:
        return
    if contains_banned_pattern(message.content):
        try:
            await message.delete()
        except discord.Forbidden:
            print("❌ Missing permissions to delete messages.")
        except discord.HTTPException as e:
            print(f"❌ Failed to delete message: {e}")
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    if after.author.bot or after.pinned or not after.guild:
        return
    guild_data = get_guild_data(after.guild.id)
    if after.author.id in guild_data["users"]:
        return
    if after.channel.id in guild_data["channels"]:
        return
    if contains_banned_pattern(after.content):
        try:
            await after.delete()
        except discord.Forbidden:
            print("Missing permissions to delete edited messages.")
        except discord.NotFound:
            pass


@bot.tree.command(name="excludeuser", description="Exclude a user from filtering in this server.")
@app_commands.checks.has_permissions(administrator=True)
async def exclude_user(interaction: discord.Interaction, user: discord.User):
    guild_data = get_guild_data(interaction.guild_id)
    if user.id not in guild_data["users"]:
        guild_data["users"].append(user.id)
        save_exclusions()
        await interaction.response.send_message(
            f"{user.mention} is now excluded in **{interaction.guild.name}**.", ephemeral=True
        )
    else:
        await interaction.response.send_message(f"{user.mention} is already excluded.", ephemeral=True)

@bot.tree.command(name="unexcludeuser", description="Remove a user from the exclusion list.")
@app_commands.checks.has_permissions(administrator=True)
async def unexclude_user(interaction: discord.Interaction, user: discord.User):
    guild_data = get_guild_data(interaction.guild_id)
    if user.id in guild_data["users"]:
        guild_data["users"].remove(user.id)
        save_exclusions()
        await interaction.response.send_message(
            f"{user.mention} is no longer excluded in **{interaction.guild.name}**.", ephemeral=True
        )
    else:
        await interaction.response.send_message(f"{user.mention} is not excluded.", ephemeral=True)

@bot.tree.command(name="excludechannel", description="Exclude a channel from filtering in this server.")
@app_commands.checks.has_permissions(administrator=True)
async def exclude_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_data = get_guild_data(interaction.guild_id)
    if channel.id not in guild_data["channels"]:
        guild_data["channels"].append(channel.id)
        save_exclusions()
        await interaction.response.send_message(
            f"{channel.mention} is now excluded in **{interaction.guild.name}**.", ephemeral=True
        )
    else:
        await interaction.response.send_message(f"{channel.mention} is already excluded.", ephemeral=True)

@bot.tree.command(name="unexcludechannel", description="Remove a channel from the exclusion list.")
@app_commands.checks.has_permissions(administrator=True)
async def unexclude_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    guild_data = get_guild_data(interaction.guild_id)
    if channel.id in guild_data["channels"]:
        guild_data["channels"].remove(channel.id)
        save_exclusions()
        await interaction.response.send_message(
            f"{channel.mention} is no longer excluded in **{interaction.guild.name}**.", ephemeral=True
        )
    else:
        await interaction.response.send_message(f"{channel.mention} is not excluded.", ephemeral=True)

@bot.tree.command(name="showexclusions", description="Show all excluded users and channels in this server.")
@app_commands.checks.has_permissions(administrator=True)
async def show_exclusions(interaction: discord.Interaction):
    guild_data = get_guild_data(interaction.guild_id)
    users = ", ".join(f"<@{uid}>" for uid in guild_data["users"]) or "None"
    channels = ", ".join(f"<#{cid}>" for cid in guild_data["channels"]) or "None"
    await interaction.response.send_message(
        f"**Excluded Users:** {users}\n**Excluded Channels:** {channels}", ephemeral=True
    )

bot.run(os.getenv("TOKEN"))
