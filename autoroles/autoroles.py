import os
import json
import discord
from discord.ext import commands
from discord import app_commands

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA config.json for autoroles was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

class AutorolesCog(commands.Cog):
    lock = False

    group = app_commands.Group(name="autoroles", description="Manage lines")

    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.group, guild=discord.Object(id=self.bot.server))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        role_ids = config.get("roles", [])
        for role_id in role_ids:
            role = guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role, reason="Autoroles assignment")
                except discord.Forbidden:
                    print(f"Missing permissions to assign role {role.name} to {member.name}.")
                except discord.HTTPException as e:
                    print(f"Failed to assign role {role.name} to {member.name}: {e}")

    @group.command(name="reload", description="reload the autoroles configuration")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("somebody's got a lock on the autoroles config. wait a sec, and try againw", ephemeral=True)
            return
        self.lock = True
        global config
        if not os.path.isfile(config_path):
            await interaction.response.send("a config.json for autoroles was not found!! please read the README for setup instructions", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        print(f"{interaction.user.name} ({interaction.user.id}) reloaded the quotes configuration.")
        await interaction.followup.send("autoroles configuration reloaded successfully", ephemeral=True)
        self.lock = False
    
    

async def setup(squishy) -> None:
    print("Loading autoroles extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA config.json for autoroles was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    await squishy.add_cog(AutorolesCog(squishy))
    print("AutorolesCog loaded")