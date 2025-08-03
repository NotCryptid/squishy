# TODO: Leaderboard, rewards

import os
import json
import random
import time
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.abc import Messageable
from datahandler import Levelling as userdata

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA config.json for levelling was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

class LevellingCog(commands.Cog):
    lock = False

    group = app_commands.Group(name="level", description="Manage levelling")
    xpgroup = app_commands.Group(name="xp", description="Manage XP")
    levelgroup = app_commands.Group(name="level", description="Manage levels")

    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.group, guild=discord.Object(id=self.bot.server))
        self.vccheck_loop = None
        self.start_vccheck_loop()

    # Re/Starts the VC XP function
    def start_vccheck_loop(self):
        cooldown = config.get("xp", {}).get("voice", {}).get("cooldown", 180)
        async def loop_body():
            await self.vccheck()
        if self.vccheck_loop and self.vccheck_loop.is_running():
            self.vccheck_loop.cancel()

        @tasks.loop(seconds=cooldown)
        async def vcloop():
            await loop_body()

        self.vccheck_loop = vcloop
        self.vccheck_loop.start()

    # Check level requirement
    def levelrequirement(self, level):
        if config.get("xp", {}).get("formula", {}).get("type", 2) == 1:
            return((level*100) + 75)
        if config.get("xp", {}).get("formula", {}).get("type", 2) == 2:
            return(5 * (level**2) + (level*50) + 75)
        if config.get("xp", {}).get("formula", {}).get("type", 2) == 3:
            return(1000)

    # Convert numbers to ordinals
    def ordinal(self, n):
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return str(n) + suffix
    
    # Calculate XP, taking into account channel and role boosters/restrictions
    async def xp_calc(self, xp: int, roles: list, channel: int):
        # Grab restrictions
        blacklist = config.get("restrictions", {}).get("blacklist", {})
        whitelist = config.get("restrictions", {}).get("whitelist", {})

        # Convert role IDs to strings for comparing
        role_ids_str = [str(role_id) for role_id in roles]

        if blacklist.get("enabled", False):
            if str(channel) in blacklist.get("channels", []):
                return(0)
            if any(role_id in blacklist.get("roles", []) for role_id in role_ids_str):
                return(0)

        if whitelist.get("enabled", False):
            if str(channel) not in whitelist.get("channels", []):
                return(0)
            if not any(role_id in whitelist.get("roles", []) for role_id in role_ids_str):
                return(0)

        # Apply role boosters
        role_boosters = config.get("boosters", {}).get("roles", {})
        for role_id in role_ids_str:
            if role_id in role_boosters:
                xp += int(xp * (role_boosters[role_id] / 100))

        # Apply channel booster
        channel_boosters = config.get("boosters", {}).get("channels", {})
        if str(channel) in channel_boosters:
            xp += int(xp * (channel_boosters[str(channel)] / 100))
        return(xp)

    # Replace {variables} in user-defined messages
    async def replace_variables(self, text, member):
        guild = await self.bot.fetch_guild(self.bot.server)
        member_count = guild.member_count or 0
        values = {
            "user.xp": userdata.getxp(None, member.id),
            "user.lvl": userdata.getlevel(None, member.id),
            "user.at": member.name,
            "user.id": member.id,
            "user.display": member.display_name,
            "user.mention": member.mention,
            "user.avatar": member.display_avatar.url if member.display_avatar else f"https://cdn.discordapp.com/embed/avatars/{int(member.id) % 5}.png",
            "server.name": guild.name,
            "server.id": guild.id,
            "server.icon": guild.icon.url if guild.icon else "https://cdn.discordapp.com/embed/avatars/1.png",
            "membercount": member_count,
            "membercount.format": self.ordinal(member_count),
            "time": int(discord.utils.utcnow().timestamp()),
            "time.iso": discord.utils.utcnow().isoformat(),
        }
        for key, value in values.items():
            text = text.replace("{" + key + "}", str(value))
        return text

    # Level-up message system
    async def levelmessage(self, send_to_channel: Messageable, member: discord.Member):
        if config.get("message", {}).get("channel", False):
            message = await self.replace_variables(config.get("message", {}).get("content", ""), member)
            embeds = [
                discord.Embed.from_dict(embed)
                for embed in json.loads(
                    await self.replace_variables(
                        json.dumps(config.get("message", {}).get("embeds", [])), member
                    )
                )
            ] if "embeds" in config.get("message", {}) else None
            await send_to_channel.send(message, embeds=embeds)
        if config.get("message", {}).get("dm", {}).get("enabled", False):
            message = await self.replace_variables(config.get("message", {}).get("dm", {}).get("content", ""), member)
            embeds = [
                discord.Embed.from_dict(embed)
                for embed in json.loads(
                    await self.replace_variables(
                        json.dumps(config.get("message", {}).get("embeds", [])), member
                    )
                )
            ] if "embeds" in config.get("message", {}) else None
            await member.send(message, embeds=embeds)

    # VC XP
    async def vccheck(self):
        if config.get("xp", {}).get("voice", {}).get("enabled", False):
            for channel in self.bot.get_guild(self.bot.server).voice_channels:
                for member in channel.members:
                    if config.get("xp", {}).get("voice", {}).get("enabled", False).get("anti-afk", False) and len(channel.members) >= config.get("xp", {}).get("voice", {}).get("enabled", False).get("minimum-members", 0):
                        if not userdata.getlastvcafk(None, member.id):
                            xp_earned = random.randint(config.get("xp", {}).get("reaction", {}).get("min", 25),
                                                       config.get("xp", {}).get("reaction", {}).get("max", 25))
                            xp_earned = await self.xp_calc(xp_earned,
                                               [role.id for role in member.roles],
                                               channel.id)
                            userdata.addxp(None, member.id, xp_earned)
                            userdata.setlastreaction(None, member.id, int(time.time()))
                            if userdata.getxp(None, member.id) >= self.levelrequirement(userdata.getlevel(None, member.id)):
                                userdata.addlevel(None, member.id, 1)
                                userdata.setxp(None, member.id, 0)
                                await self.levelmessage(channel, member)
                        if member.voice.mute or member.voice.self_mute:
                            userdata.setlastvcafk(None, member.id, True)
                        else:
                            userdata.setlastvcafk(None, member.id, False)
                    else:
                        userdata.addxp(None, member.id, random.randint(config.get("xp", {}).get("reaction", {}).get("min", 25), config.get("xp", {}).get("reaction", {}).get("max", 25)))
                        userdata.setlastreaction(None, member.id, int(time.time()))
                        if userdata.getxp(None, member.id) >= self.levelrequirement(userdata.getlevel(None, member.id)) and len(channel.members) >= config.get("xp", {}).get("voice", {}).get("enabled", False).get("minimum-members", 0):
                            userdata.addlevel(None, member.id, 1)
                            userdata.setxp(None, member.id, 0)
                            await self.levelmessage(channel, member)

    @group.command(name="leaderboard", description="Get a leaderboard of the server's levels and XP!")
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if not config.get("leaderboard", {}).get("enabled", True):
            await interaction.followup.send("The leaderboard feature is disabled.", ephemeral=True)
            return

        entries = config.get("leaderboard", {}).get("entries", 10)
        top_users = userdata.xptop(None, entries)
        embed = discord.Embed(title="Leaderboard", color=0x8A2BE2)

        for index, user_id in enumerate(top_users, start=1):
            try:
                member = await self.bot.fetch_user(user_id)
            except discord.NotFound:
                continue

            level = userdata.getlevel(None, user_id)
            xp = userdata.getxp(None, user_id)
            required = self.levelrequirement(level)

            progress_ratio = min(max(xp / required, 0), 1) if required else 0
            filled = int(progress_ratio * 10)
            empty = 10 - filled
            bar = ":purple_square:" * filled + ":black_large_square:" * empty
            percent = int(progress_ratio * 100)

            embed.add_field(
                name=f"#{index} - [LVL {level}] {member.name}",
                value=f"{bar} `{percent}%`",
                inline=False
            )

        await interaction.followup.send(embed=embed)

    # Config reload
    @group.command(name="reload", description="Reload the level configuration")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("Somebody's got a lock on the levelling config. Wait a sec, and try again.", ephemeral=True)
            return
        self.lock = True
        global config
        if not os.path.isfile(config_path):
            await interaction.followup.send("A config.json for levelling was not found!! Please read the README for setup instructions.", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        print(f"{interaction.user.name} ({interaction.user.id}) reloaded the levelling configuration.")
        self.start_vccheck_loop()
        await interaction.followup.send("Levelling configuration reloaded successfully.", ephemeral=True)
        self.lock = False
    
    @xpgroup.command(name="set", description="Set a users XP")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def xpset(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        amount = max(0, min(amount, self.levelrequirement(userdata.getlevel(None, member.id))-1))
        userdata.setxp(None, member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) set {member.name}'s ({member.id}) XP to {amount}.")
        await interaction.followup.send(f"Set {member.mention}'s XP to {amount}\n-# This may have been capped to (next level requirement-1) or 0.", ephemeral=True)

    @xpgroup.command(name="add", description="Give a user XP")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def xpadd(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        amount = min(amount, self.levelrequirement(userdata.getlevel(None, member.id))-1)
        userdata.addxp(None, member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) gave {member.name} ({member.id}) {amount}XP.")
        await interaction.followup.send(f"Gave {member.mention} {amount}XP\n-# This may have been capped to (next level requirement-1).", ephemeral=True)

    @xpgroup.command(name="take", description="Take a user's XP")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def xptake(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        amount = min(amount, userdata.getxp(None, member.id))
        userdata.takexp(None, member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) took {amount}XP from {member.name} ({member.id}).")
        await interaction.followup.send(f"Took {amount}XP from {member.mention}\n-# This may have been capped to prevent them from going below 0.", ephemeral=True)

    # Add XP subgroup to level group
    group.add_command(xpgroup)

    @levelgroup.command(name="set", description="Set a user's level")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setlevel(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        max_level = config.get("xp", {}).get("formula", {}).get("max-level", 0)
        if max_level > 0:
            amount = min(amount, max_level)
        if amount <= 0:
            amount = 1
        userdata.setlevel(None, member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) set {member.name}'s ({member.id}) level to {amount}.")
        await interaction.followup.send(f"Set {member.mention}'s level to {amount}.\n-# This may have been capped to respect a minimum level of 1 or the level cap.", ephemeral=True)

    @levelgroup.command(name="add", description="Add to a user's level")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def addlevel(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        current_level = userdata.getlevel(None, member.id)
        max_level = config.get("xp", {}).get("formula", {}).get("max-level", 0)
        if max_level > 0:
            amount = min(amount, max(0, max_level - current_level))
        userdata.addlevel(None, member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) added {amount} levels to {member.name} ({member.id}).\n-# This may have been capped to respect the level cap.")
        await interaction.followup.send(f"Added {amount} levels to {member.mention}.", ephemeral=True)

    @levelgroup.command(name="take", description="Take levels from a user")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def takelevel(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        current_level = userdata.getlevel(None, member.id)
        if current_level - amount <= 0:
            amount = current_level-1
        userdata.takelevel(None, member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) took {amount} levels from {member.name} ({member.id}).")
        await interaction.followup.send(f"Took {amount} levels from {member.mention}.\n-# This may have been capped to respect a minimum level of 1.", ephemeral=True)

    # Add level subgroup to level group
    group.add_command(levelgroup)

    # Message XP
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if config.get("xp", {}).get("message", {}).get("enabled", False):
            lastmessage = userdata.getlastmessage(None, message.author.id)
            cooldown = config.get("xp", {}).get("message", {}).get("cooldown", 60)
            if lastmessage == 0 or int(time.time()) - lastmessage >= cooldown:
                xp_earned = random.randint(config.get("xp", {}).get("message", {}).get("min", 15),
                                           config.get("xp", {}).get("message", {}).get("max", 40))
                if config.get("boosters", {}).get("effort", {}).get("enabled", False):
                    words = len(message.content.split())
                    words_per_boost = config.get("boosters", {}).get("effort", {}).get("words", 25)
                    percent = config.get("boosters", {}).get("effort", {}).get("percent", 10)
                    boost_multiplier = (words // words_per_boost) * (percent / 100)
                    xp_earned = int(xp_earned * (1 + boost_multiplier))
                xp_earned = await self.xp_calc(xp_earned,
                                               [role.id for role in message.author.roles],
                                               message.channel.id)
                userdata.addxp(None, message.author.id, xp_earned)
                userdata.setlastmessage(None, message.author.id, int(time.time()))
            levelreq = self.levelrequirement(userdata.getlevel(None, message.author.id))
            if userdata.getxp(None, message.author.id) >= levelreq:
                userdata.addlevel(None, message.author.id, 1)
                userdata.setxp(None, message.author.id, 0)
                await self.levelmessage(message.channel, message.author)

    # Reaction XP
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = await self.bot.fetch_user(payload.user_id)
        channel = await self.bot.fetch_channel(payload.channel_id)
        if user.bot:
            return
        if config.get("xp", {}).get("reaction", {}).get("enabled", False):
            lastmessage = userdata.getlastreaction(None, user.id)
            cooldown = config.get("xp", {}).get("reaction", {}).get("cooldown", 300)
            if lastmessage == 0 or int(time.time()) - lastmessage >= cooldown:
                xp_earned = random.randint(config.get("xp", {}).get("reaction", {}).get("min", 25),
                                           config.get("xp", {}).get("reaction", {}).get("max", 25))
                xp_earned = await self.xp_calc(xp_earned,
                                               [role.id for role in user.roles],
                                               channel.id)
                userdata.addxp(None, user.id, xp_earned)
                userdata.setlastreaction(None, user.id, int(time.time()))
            levelreq = self.levelrequirement(userdata.getlevel(None, user.id))
            if userdata.getxp(None, user.id) >= levelreq:
                userdata.addlevel(None, user.id, 1)
                userdata.setxp(None, user.id, 0)
                await self.levelmessage(channel, user)


async def setup(squishy) -> None:
    print("Loading levelling extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA config.json for levelling was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    await squishy.add_cog(LevellingCog(squishy))
    print("LevellingCog loaded")