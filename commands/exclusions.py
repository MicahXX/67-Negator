import discord
from discord import app_commands
from discord.ext import commands
from utils.exclusions import get_guild_data, save_all


class ExclusionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Exclude a user
    @app_commands.command(name="excludeuser", description="Exclude a user from filtering.")
    @app_commands.checks.has_permissions(administrator=True)
    async def exclude_user(self, interaction: discord.Interaction, user: discord.User):
        guild_data = get_guild_data(interaction.guild_id)
        if user.id not in guild_data["users"]:
            guild_data["users"].append(user.id)
            save_all()
            await interaction.response.send_message(f"{user.mention} will now be excluded.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} is already excluded.", ephemeral=True)

    # Unexclude a user
    @app_commands.command(name="unexcludeuser", description="Remove a user from exclusions.")
    @app_commands.checks.has_permissions(administrator=True)
    async def unexclude_user(self, interaction: discord.Interaction, user: discord.User):
        guild_data = get_guild_data(interaction.guild_id)
        if user.id in guild_data["users"]:
            guild_data["users"].remove(user.id)
            save_all()
            await interaction.response.send_message(f"{user.mention} will now be unexcluded.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} is not excluded.", ephemeral=True)

    # Exclude a channel
    @app_commands.command(name="excludechannel", description="Exclude a channel from filtering.")
    @app_commands.checks.has_permissions(administrator=True)
    async def exclude_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_data = get_guild_data(interaction.guild_id)
        if channel.id not in guild_data["channels"]:
            guild_data["channels"].append(channel.id)
            save_all()
            await interaction.response.send_message(f"{channel.mention} will now be excluded.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{channel.mention} is already excluded.", ephemeral=True)

    # Unexclude a channel
    @app_commands.command(name="unexcludechannel", description="Remove a channel from exclusions.")
    @app_commands.checks.has_permissions(administrator=True)
    async def unexclude_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_data = get_guild_data(interaction.guild_id)
        if channel.id in guild_data["channels"]:
            guild_data["channels"].remove(channel.id)
            save_all()
            await interaction.response.send_message(f"{channel.mention} will now be unexcluded again.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{channel.mention} is not excluded.", ephemeral=True)

    # Show exclusions
    @app_commands.command(name="showexclusions", description="Show all excluded users and channels.")
    @app_commands.checks.has_permissions(administrator=True)
    async def show_exclusions(self, interaction: discord.Interaction):
        guild_data = get_guild_data(interaction.guild_id)
        users = ", ".join(f"<@{u}>" for u in guild_data["users"]) or "None"
        channels = ", ".join(f"<#{c}>" for c in guild_data["channels"]) or "None"
        await interaction.response.send_message(
            f"**Excluded Users:** {users}\n**Excluded Channels:** {channels}",
        )


async def setup(bot):
    await bot.add_cog(ExclusionCommands(bot))