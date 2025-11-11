import discord
from discord.ext import commands
from utils.exclusions import get_guild_data

BANNED_EMOJIS = {"🤰", "🫃", "🫄", "6️⃣", "7️⃣"}


class OnReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return
        if not reaction.message.guild:
            return

        guild_data = get_guild_data(reaction.message.guild.id)

        if user.id in guild_data["users"]:
            return
        if reaction.message.channel.id in guild_data["channels"]:
            return

        emoji_str = str(reaction.emoji)

        if isinstance(reaction.emoji, discord.PartialEmoji):
            emoji_str = reaction.emoji.name

        if emoji_str in BANNED_EMOJIS:
            try:
                await reaction.remove(user)
            except discord.Forbidden:
                print("Missing permissions to remove reactions.")
            except discord.HTTPException as e:
                print(f"Failed to remove reaction: {e}")


async def setup(bot):
    await bot.add_cog(OnReaction(bot))
