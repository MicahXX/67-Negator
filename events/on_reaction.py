import discord
from discord.ext import commands
from utils.exclusions import get_guild_data

BANNED_EMOJIS = {"🤰", "🫃", "🫄", "6️⃣", "7️⃣"}

class OnReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.bot or not reaction.message.guild:
            return

        guild_data = get_guild_data(reaction.message.guild.id)
        if user.id in guild_data.get("users", []):
            return
        if reaction.message.channel.id in guild_data.get("channels", []):
            return

        emoji = reaction.emoji

        if isinstance(emoji, discord.PartialEmoji):
            return

        if isinstance(emoji, str) and emoji in BANNED_EMOJIS:
            try:
                await reaction.remove(user)
            except discord.Forbidden:
                print("Missing permissions to remove reactions.")
            except discord.HTTPException as e:
                print(f"Failed to remove reaction: {e}")

async def setup(bot):
    await bot.add_cog(OnReaction(bot))
