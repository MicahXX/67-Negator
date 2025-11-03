import discord
from discord.ext import commands
from utils.filters import contains_banned_pattern
from utils.exclusions import get_guild_data

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
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
                print("Missing permissions to delete messages.")
            except discord.HTTPException as e:
                print(f"Failed to delete message: {e}")

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(OnMessage(bot))
