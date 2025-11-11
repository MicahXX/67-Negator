import discord
from discord.ext import commands

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

        emoji_str = str(reaction.emoji)
        if emoji_str in BANNED_EMOJIS:
            try:
                await reaction.remove(user)
            except discord.Forbidden:
                print("Missing permissions to remove reactions.")
            except discord.HTTPException:
                print("Failed to remove reaction.")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        pass

async def setup(bot):
    await bot.add_cog(OnReaction(bot))
