import discord
from discord.ext import commands

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print(f"Logged in as {self.bot.user} — Slash commands synced.")
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="STOP THE NUMBER",
            )
        )

async def setup(bot):
    await bot.add_cog(OnReady(bot))