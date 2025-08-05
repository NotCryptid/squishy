import os
import json
import discord
from discord.ext import commands
from discord import app_commands

config_path = os.path.join(os.path.dirname(__file__), "extensiontemplate-config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA extensiontemplate-config.json for extensiontemplate was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

class ExtensiontemplateCog(commands.Cog):
    lock = False

    group = app_commands.Group(name="extensiontemplate", description="Manage extensiontemplate")

    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.group, guild=discord.Object(id=self.bot.server))

    @group.command(name="reload", description="reload the extensiontemplate configuration")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("somebody's got a lock on the extensiontemplate config. wait a sec, and try againw", ephemeral=True)
            return
        self.lock = True
        global config
        if not os.path.isfile(config_path):
            await interaction.response.send("a config.json for extensiontemplate was not found!! please read the README for setup instructions", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        print(f"{interaction.user.name} ({interaction.user.id}) reloaded the quotes configuration.")
        await interaction.followup.send("extensiontemplate configuration reloaded successfully", ephemeral=True)
        self.lock = False

    @group.command(name="ping", description="pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("Pong!")

async def setup(squishy) -> None:
    print("Loading extensiontemplate extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA extensiontemplate-config.json for extensiontemplate was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    await squishy.add_cog(ExtensiontemplateCog(squishy))
    print("ExtensiontemplateCog loaded")