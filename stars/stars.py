import os
import json
import random
import discord
from discord.ext import commands
from discord import app_commands
from datahandler import Economy

userdata = Economy()

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA config.json for stars was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

class StarsCog(commands.Cog):
    lock = False

    group = app_commands.Group(name="stars", description="Manage lines")

    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.group, guild=discord.Object(id=self.bot.server))

    @group.command(name="reload", description="reload the stars configuration")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("somebody's got a lock on the stars config. wait a sec, and try againw", ephemeral=True)
            return
        self.lock = True
        global config
        if not os.path.isfile(config_path):
            await interaction.response.send("a config.json for stars was not found!! please read the README for setup instructions", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        print(f"{interaction.user.name} ({interaction.user.id}) reloaded the quotes configuration.")
        await interaction.followup.send("stars configuration reloaded successfully", ephemeral=True)
        self.lock = False

    @group.command(name="give", description="give a star to a member")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def give(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.response.defer()
        giverole = config.get("give-role", 0)
        executorroles = [role.id for role in interaction.user.roles]
        memberroles = [role.id for role in member.roles]
        if giverole not in executorroles:
            await interaction.followup.send("you don't have permission to give stars", ephemeral=True)
            return
        if member.id == interaction.user.id and not config.get("can-give-self", False) or giverole in memberroles and not config.get("can-give-eachother", False):
            await interaction.followup.send("you can't give to them", ephemeral=True)
            return
        userdata.addstars(member.id, 1)
        await interaction.followup.send(f"{interaction.user.mention} gave a star to {member.mention} for \"{reason}\"\n{member.mention} now has {userdata.getstars(member.id)} stars")

    @group.command(name="take", description="take a star from a member")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def take(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.response.defer()
        takerole = config.get("take-role", 0)
        executorroles = [role.id for role in interaction.user.roles]
        memberroles = [role.id for role in member.roles]
        if takerole not in executorroles:
            await interaction.followup.send("you don't have permission to take stars", ephemeral=True)
            return
        if member.id == interaction.user.id and not config.get("can-take-self", False) or takerole in memberroles and not config.get("can-take-eachother", False):
            await interaction.followup.send("you can't take from them", ephemeral=True)
            return
        if userdata.getstars(member.id) < 1:
            await interaction.followup.send("you can't take from them", ephemeral=True)
            return
        userdata.takestars(member.id, 1)
        await interaction.followup.send(f"{interaction.user.mention} took a star from {member.mention} for \"{reason}\"\n{member.mention} now has {userdata.getstars(member.id)} stars")

    @group.command(name="smash", description="smash a star into currency")
    async def smash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if not config.get("can-smash", False):
            await interaction.followup.send("smashing stars is disabled", ephemeral=True)
            return
        if not "economy.economy" in self.bot.extensions:
            await interaction.followup.send("the economy module is not loaded", ephemeral=True)
            return
        if userdata.getstars(interaction.user.id) < 1:
            await interaction.followup.send("you don't have any stars to smash", ephemeral=True)
            return
        userdata.takestars(interaction.user.id, 1)
        amount = random.randint(config.get("smash-min", 10), config.get("smash-max", 20))
        userdata.addbal(interaction.user.id, amount)

        economy_config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "economy", "config.json")
        with open(economy_config_path, "r", encoding="utf-8") as economy_file:
            economy_config = json.load(economy_file)

        def formatcurrency(amount):
            amount = str(amount)
            if economy_config.get("currency-placement", 2) == 1:
                amount = ''.join([economy_config.get("currency-symbol", "$"), amount])
            else:
                amount = ''.join([amount, economy_config.get("currency-symbol", "$")])
            return(amount)

        await interaction.followup.send(f"you smashed a star and received {formatcurrency(amount)}!", ephemeral=True)

async def setup(squishy) -> None:
    print("Loading stars extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA config.json for stars was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    await squishy.add_cog(StarsCog(squishy))
    print("StarsCog loaded")