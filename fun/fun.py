import os
import json
import random
import discord
from discord import app_commands
from discord.ext import commands
from datahandler import Economy

userdata = Economy()

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA config.json for fun was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

economy_config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "economy", "config.json")
with open(economy_config_path, "r", encoding="utf-8") as economy_file:
    economy_config = json.load(economy_file)

class FunCog(commands.Cog):
    lock = False

    group = app_commands.Group(name="fun", description="Manage fun")

    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.group, guild=discord.Object(id=self.bot.server))

    def formatcurrency(self, amount):
        amount = str(amount)
        if economy_config.get("currency-placement", 2) == 1:
            amount = ''.join([economy_config.get("currency-symbol", "$"), amount])
        else:
            amount = ''.join([amount, economy_config.get("currency-symbol", "$")])
        return(amount)

    @group.command(name="reload", description="reload the fun configuration")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("somebody's got a lock on the fun config. wait a sec, and try againw", ephemeral=True)
            return
        self.lock = True
        global config
        if not os.path.isfile(config_path):
            await interaction.response.send("a config.json for fun was not found!! please read the README for setup instructions", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        print(f"{interaction.user.name} ({interaction.user.id}) reloaded the quotes configuration.")
        await interaction.followup.send("fun configuration reloaded successfully", ephemeral=True)
        self.lock = False

    @group.command(name="coinflip", description="do a coinflip")
    async def coinflip(self, interaction: discord.Interaction, bet: int):
        await interaction.response.defer(ephemeral=True)
        conf = config.get("coinflip", {})
        if conf.get("enabled", False):
            maxbet = conf.get("maxbet", 25)
            minbet = conf.get("minbet", 10)
            if bet > maxbet:
                await interaction.followup.send(embed=discord.Embed(
                    colour=discord.Colour.red(),
                    title="bruh",
                    description=f"bet cannot exceed {maxbet}"
                ))
                return
            if bet < minbet:
                await interaction.followup.send(embed=discord.Embed(
                    colour=discord.Colour.red(),
                    title="bruh",
                    description=f"bet must be more than {minbet}"
                ))
                return
            if bet > userdata.getbal(interaction.user.id):
                await interaction.followup.send(embed=discord.Embed(
                    colour=discord.Colour.red(),
                    title="bruh",
                    description=f"you don't have {bet} {economy_config.get('currency-name-plural', 'money')}"
                ))
                return
            if random.randint(0, 1):
                userdata.addbal(interaction.user.id, round(bet*0.5))
                await interaction.followup.send(embed=discord.Embed(
                    colour=discord.Colour.green(),
                    title="huzzah",
                    description=f"you won {round(bet*0.5)} {economy_config.get('currency-name-plural', 'money')}"
                ))
                return
            else:
                userdata.takebal(interaction.user.id, bet)
                await interaction.followup.send(embed=discord.Embed(
                    colour=discord.Colour.red(),
                    title="oof",
                    description=f"you lost {bet}"
                ))
                return




async def setup(squishy) -> None:
    print("Loading fun extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA config.json for fun was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    await squishy.add_cog(FunCog(squishy))
    print("FunCog loaded")

