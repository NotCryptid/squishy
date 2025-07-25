import os
import json
import random
from discord.ext import commands

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA config.json for quotes was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

class QuotesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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