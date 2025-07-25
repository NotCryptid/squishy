import os
import json
import asyncio
import discord
from discord.ext import commands

with open(os.path.join(os.path.dirname(__file__), "config.json"), "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

onreadyIsTheWorstFuckingThingEver = False
squishy = commands.Bot(command_prefix=lambda *_: [], intents=discord.Intents.all())
squishy.server = config.get("server-id", 0)

async def cleanup():
    while True:
        for guild in squishy.guilds:
            if guild.id != squishy.server:
                print(f"Leaving bad server: {guild.name} ({guild.id})")
                await guild.leave()
        await asyncio.sleep(60)

@squishy.event
async def on_ready():
    global onreadyIsTheWorstFuckingThingEver
    if not onreadyIsTheWorstFuckingThingEver:
        print(f"Logged in as {squishy.user.name} ({squishy.user.id})")
        if config.get("modules", {}).get("quotes", False):
            await squishy.load_extension("quotes.quotes")
        if config.get("modules", {}).get("welcome", False):
            await squishy.load_extension("welcome.welcome")
        await squishy.tree.sync(guild=discord.Object(id=squishy.server))
        squishy.loop.create_task(cleanup())
        onreadyIsTheWorstFuckingThingEver = True

squishy.run(config.get("bot-token", "CHANGEME"))