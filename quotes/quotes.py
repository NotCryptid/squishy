import os
import json
import random
import discord
from discord.ext import commands
from discord import app_commands

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA config.json for quotes was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

class QuotesCog(commands.Cog):
    lock = False

    group = app_commands.Group(name="quotes", description="Manage quotes")

    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.group, guild=discord.Object(id=self.bot.server))

    async def quote_autocomplete(self, interaction: discord.Interaction, current: str):
        quotes = config.get("quotes", [])
        return [
            discord.app_commands.Choice(
                name=f"{i+1}: {quote[:80]}{'...' if len(quote) > 80 else ''}",
                value=str(i)
            )
            for i, quote in enumerate(quotes)
            if current.lower() in quote.lower()
        ][:25]

    @group.command(name="reload", description="Reload the quotes configuration")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("Somebody's got a lock on the quotes config. Wait a sec, and try again.", ephemeral=True)
            return
        self.lock = True
        global config
        if not os.path.isfile(config_path):
            await interaction.response.send_message("A config.json for quotes was not found!! Please read the README for setup instructions.", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        print(f"{interaction.user.name} ({interaction.user.id}) reloaded the quotes configuration.")
        await interaction.followup.send("Quotes configuration reloaded successfully.", ephemeral=True)
        self.lock = False

    @group.command(name="add", description="Add a new quote")
    @app_commands.describe(quote="The quote to add")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def add(self, interaction: discord.Interaction, quote: str):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("Somebody's got a lock on the quotes config. Wait a sec, and try again.", ephemeral=True)
            return
        self.lock = True
        if not os.path.isfile(config_path):
            await interaction.followup.send("A config.json for quotes was not found!! Please read the README for setup instructions.", ephemeral=True)
            self.lock = False
            return
        if "quotes" not in config:
            config["quotes"] = []
        config["quotes"].append(quote)
        with open(config_path, "w", encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4)
        print(f"{interaction.user.name} ({interaction.user.id}) added a new quote: {quote}")
        await interaction.followup.send(f"Quote added: {quote}", ephemeral=True)
        self.lock = False

    @group.command(name="remove", description="Remove a quote by index")
    @app_commands.autocomplete(index=quote_autocomplete)
    @app_commands.describe(index="The quote to remove")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove(self, interaction: discord.Interaction, index: str):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("Somebody's got a lock on the quotes config. Wait a sec, and try again.", ephemeral=True)
            return
        self.lock = True
        if not os.path.isfile(config_path):
            await interaction.followup.send("A config.json for quotes was not found!! Please read the README for setup instructions.", ephemeral=True)
            return
        try:
            idx = int(index)
            removed_quote = config["quotes"].pop(idx)
        except (ValueError, IndexError):
            await interaction.followup.send("Invalid quote index.", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "w", encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4)
        print(f"{interaction.user.name} ({interaction.user.id}) removed quote \"{removed_quote}\"")
        await interaction.followup.send(f"Removed quote: {removed_quote}", ephemeral=True)
        self.lock = False

    def replace_variables(self, text, member):
        values = {
            "user.mention": member.mention,
            "server.name": member.guild.name,
            "membercount": member.guild.member_count
        }
        for key, value in values.items():
            text = text.replace("{" + key + "}", str(value))
        return text
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if f"<@{self.bot.user.id}>" in message.content:
            quotes = config.get("quotes", ["Put your quotes here!\n-# If you're a user, nag the owner to add some."])
            await message.reply("\n".join([config.get("prefix", ""), random.choice(quotes) + config.get("suffix", "")]))

async def setup(squishy) -> None:
    print("Loading quotes extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA config.json for welcome was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    await squishy.add_cog(QuotesCog(squishy))
    print("QuotesCog loaded")