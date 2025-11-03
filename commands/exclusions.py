from discord import app_commands
from discord.ext import commands
from utils.exclusions import get_guild_data, load_exclusions, save_exclusions

exclusions = load_exclusions()

class ExclusionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="excludeuser", description="Exclude a user from filtering.")
    @app_commands.checks.has_permissions(administrator=True)
    async def exclude_user(self, interaction, user):
        guild_data = get_guild_data(exclusions, interaction.guild_id)
        if user.id not in guild_data["users"]:
            guild_data["users"].append(user.id)
            save_exclusions(exclusions)
            await interaction.response.send_message(f"{user.mention} excluded.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} already excluded.", ephemeral=True)

    @app_commands.command(name="unexcludeuser", description="Remove a user from exclusions.")
    @app_commands.checks.has_permissions(administrator=True)
    async def unexclude_user(self, interaction, user):
        guild_data = get_guild_data(exclusions, interaction.guild_id)
        if user.id in guild_data["users"]:
            guild_data["users"].remove(user.id)
            save_exclusions(exclusions)
            await interaction.response.send_message(f"{user.mention} unexcluded.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} not excluded.", ephemeral=True)

    @app_commands.command(name="excludechannel", description="Exclude a channel from filtering.")
    @app_commands.checks.has_permissions(administrator=True)
    async def exclude_channel(self, interaction, channel):
        guild_data = get_guild_data(exclusions, interaction.guild_id)
        if channel.id not in guild_data["channels"]:
            guild_data["channels"].append(channel.id)
            save_exclusions(exclusions)
            await interaction.response.send_message(f"{channel.mention} excluded.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{channel.mention} already excluded.", ephemeral=True)

    @app_commands.command(name="unexcludechannel", description="Remove a channel from exclusions.")
    @app_commands.checks.has_permissions(administrator=True)
    async def unexclude_channel(self, interaction, channel):
        guild_data = get_guild_data(exclusions, interaction.guild_id)
        if channel.id in guild_data["channels"]:
            guild_data["channels"].remove(channel.id)
            save_exclusions(exclusions)
            await interaction.response.send_message(f"{channel.mention} unexcluded.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{channel.mention} not excluded.", ephemeral=True)

    @app_commands.command(name="showexclusions", description="Show all exclusions.")
    @app_commands.checks.has_permissions(administrator=True)
    async def show_exclusions(self, interaction):
        guild_data = get_guild_data(exclusions, interaction.guild_id)
        users = ", ".join(f"<@{u}>" for u in guild_data["users"]) or "None"
        channels = ", ".join(f"<#{c}>" for c in guild_data["channels"]) or "None"
        await interaction.response.send_message(
            f"**Excluded Users:** {users}\n**Excluded Channels:** {channels}",
            ephemeral=True,
        )

async def setup(bot):
    await bot.add_cog(ExclusionCommands(bot))