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

# Leave servers that aren't the primary server
async def cleanup():
    while True:
        for guild in squishy.guilds:
            if guild.id != squishy.server:
                print(f"Leaving bad server: {guild.name} ({guild.id})")
                await guild.leave()
        await asyncio.sleep(60)

# Rotate through statuses at user defined interval
async def rotate_statuses():
    while True:
        guild = squishy.get_guild(squishy.server)
        if not guild:
            await asyncio.sleep(config.get("status-interval", 30))
            continue

        statuses_to_rotate = []

        statuses_config = config.get("statuses", {})

        # Status type mapping
        online_status = config.get("online", 1)
        status_map = {
            1: discord.Status.online,
            2: discord.Status.idle,
            3: discord.Status.dnd,
            4: discord.Status.invisible,
        }
        presence_status = status_map.get(online_status, discord.Status.online)

        if statuses_config.get("member-count", False):
            member_count = guild.member_count or 0
            statuses_to_rotate.append(f"{member_count} members")

        if statuses_config.get("role-count", False):
            role_count = len(guild.roles) if guild.roles else 0
            statuses_to_rotate.append(f"{role_count} roles")

        if statuses_config.get("channel-count", False):
            channel_count = len(guild.channels) if guild.channels else 0
            statuses_to_rotate.append(f"{channel_count} channels")

        if statuses_config.get("github", False):
            statuses_to_rotate.append("github.com/enhancedrock/squishy")

        if statuses_config.get("custom-enabled", False):
            custom_text = statuses_config.get("custom", "")
            if custom_text:
                statuses_to_rotate.append(custom_text)

        if not statuses_to_rotate:
            await asyncio.sleep(config.get("status-interval", 30))
            continue

        for status_text in statuses_to_rotate:
            if status_text == statuses_config.get("custom", "") and statuses_config.get("custom-enabled", False):
                custom_type = statuses_config.get("custom-type", 2)
                if custom_type == 1:
                    activity_type = discord.ActivityType.playing
                    await squishy.change_presence(activity=discord.Activity(name=status_text, type=activity_type), status=presence_status)
                elif custom_type == 2:
                    activity_type = discord.ActivityType.watching
                    await squishy.change_presence(activity=discord.Activity(name=status_text, type=activity_type), status=presence_status)
                elif custom_type == 3:
                    activity_type = discord.ActivityType.listening
                    await squishy.change_presence(activity=discord.Activity(name=status_text, type=activity_type), status=presence_status)
                elif custom_type == 4:
                    await squishy.change_presence(activity=discord.CustomActivity(name=status_text), status=presence_status)
                else:
                    await squishy.change_presence(activity=discord.Activity(name=status_text), status=presence_status)
            else:
                # For non-custom statuses, always watching
                await squishy.change_presence(
                    activity=discord.Activity(name=status_text, type=discord.ActivityType.watching),
                    status=presence_status
                )
            await asyncio.sleep(config.get("status-interval", 30))

# I fucking hate on_ready
@squishy.event
async def on_ready():
    global onreadyIsTheWorstFuckingThingEver
    if not onreadyIsTheWorstFuckingThingEver:
        print(f"Logged in as {squishy.user.name} ({squishy.user.id})")
        if config.get("modules", {}).get("customs", False):
            premain_path = os.path.join(os.path.dirname(__file__), "customs", "premain")
            if os.path.isdir(premain_path):
                for file in sorted(os.listdir(premain_path)):
                    if file.endswith(".py") and not file.startswith("-"):
                        ext_path = f"customs.premain.{file[:-3]}"
                        try:
                            await squishy.load_extension(ext_path)
                            print(f"Loading premain extension: {ext_path}")
                        except Exception as e:
                            print(f"Failed to load premain extension {ext_path}: {e}")
        if config.get("modules", {}).get("economy", False):
            await squishy.load_extension("economy.economy")
        if config.get("modules", {}).get("catchphrase", False):
            await squishy.load_extension("catchphrase.catchphrase")
        if config.get("modules", {}).get("welcome", False):
            await squishy.load_extension("welcome.welcome")
        if config.get("modules", {}).get("levelling", False):
            await squishy.load_extension("levelling.levelling")
        if config.get("modules", {}).get("autoroles", False):
            await squishy.load_extension("autoroles.autoroles")
        if config.get("modules", {}).get("messagebuilder", False):
            await squishy.load_extension("messagebuilder.messagebuilder")
        if config.get("modules", {}).get("stars", False):
            await squishy.load_extension("stars.stars")
        if config.get("modules", {}).get("customs", False):
            premain_path = os.path.join(os.path.dirname(__file__), "customs", "premain")
            if os.path.isdir(premain_path):
                for file in sorted(os.listdir(premain_path)):
                    if file.endswith(".py") and not file.startswith("-"):
                        ext_path = f"customs.premain.{file[:-3]}"
                        try:
                            await squishy.load_extension(ext_path)
                            print(f"Loading postmain extension: {ext_path}")
                        except Exception as e:
                            print(f"Failed to load postmain extension {ext_path}: {e}")
        await squishy.tree.sync(guild=discord.Object(id=squishy.server))
        online_status = config.get("online", 1)
        status_map = {
            1: discord.Status.online,
            2: discord.Status.idle,
            3: discord.Status.dnd,
            4: discord.Status.invisible,
        }
        await squishy.change_presence(status=status_map.get(online_status, discord.Status.online))
        squishy.loop.create_task(cleanup())
        squishy.loop.create_task(rotate_statuses())
        onreadyIsTheWorstFuckingThingEver = True

# Tell a user they don't have permissions rather than letting interaction time out
@squishy.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.errors.MissingPermissions):
        await interaction.followup.send(
            "You don't have permission to use this command.",
            ephemeral=True
        )
    else:
        # Print full traceback to the console should something go wrong
        import traceback
        traceback.print_exception(type(error), error, error.__traceback__)
        try:
            await interaction.followup.send("Something went wrong while running the command! The admin has been notified.", ephemeral=True)
        except discord.InteractionResponded:
            pass

squishy.run(config.get("bot-token", "CHANGEME"))