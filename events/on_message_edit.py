from discord.ext import commands
from utils.exclusions import get_guild_data, get_ultimate_defense
from utils.filters import contains_banned_pattern
import discord


class OnMessageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot or after.pinned or not after.guild:
            return

        guild_data = get_guild_data(after.guild.id)

        if after.author.id in guild_data["users"]:
            return
        if after.channel.id in guild_data["channels"]:
            return

        if contains_banned_pattern(after.content, ultimate_defense=get_ultimate_defense(after.guild.id)):
            try:
                await after.delete()
            except discord.Forbidden:
                print("Missing permissions to delete edited messages.")
            except discord.NotFound:
                pass


async def setup(bot):
    await bot.add_cog(OnMessageEdit(bot))