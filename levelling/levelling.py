import os
import json
import random
import time
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.abc import Messageable
from datahandler import Levelling

userdata = Levelling()

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
            "user.xp": userdata.getxp(member.id),
            "user.lvl": userdata.getlevel(member.id),
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

    async def levelrewards(self, member: discord.Member, level: int):
        rewards = config.get("rewards", {})
        level_rewards = rewards.get(str(level), [])

        if "economy.economy" in self.bot.extensions:
            currency_config = rewards.get("currency", {})
            every = currency_config.get("evey-x-level")
            if every and level % every == 0:
                from datahandler import Economy
                minimum = currency_config.get("min", 0)
                maximum = currency_config.get("max", 0)
                amnt_to_give = random.randint(minimum, maximum)
                Economy.addbal(None, member.id, amnt_to_give)

        for reward_id in level_rewards:
            role = member.guild.get_role(reward_id)
            if role and role not in member.roles:
                try:
                    await member.add_roles(role, reason=f"Level reward for reaching level {level}")
                except discord.Forbidden:
                    print(f"Could not add role {role.name} to {member.display_name} due to missing permissions.")
                except discord.HTTPException as e:
                    print(f"Failed to add role {role.name} to {member.display_name}: {e}")
    
    # VC XP
    async def vccheck(self):
        if config.get("xp", {}).get("voice", {}).get("enabled", False):
            for channel in self.bot.get_guild(self.bot.server).voice_channels:
                for member in channel.members:
                    if config.get("xp", {}).get("voice", {}).get("enabled", False).get("anti-afk", False) and len(channel.members) >= config.get("xp", {}).get("voice", {}).get("enabled", False).get("minimum-members", 0):
                        if not userdata.getlastvcafk(member.id):
                            xp_earned = random.randint(config.get("xp", {}).get("reaction", {}).get("min", 25),
                                                       config.get("xp", {}).get("reaction", {}).get("max", 25))
                            xp_earned = await self.xp_calc(xp_earned,
                                               [role.id for role in member.roles],
                                               channel.id)
                            userdata.addxp(member.id, xp_earned)
                            if userdata.getxp(member.id) >= self.levelrequirement(userdata.getlevel(member.id)):
                                userdata.addlevel(member.id, 1)
                                userdata.setxp(member.id, 0)
                                await self.levelmessage(channel, member)
                                await self.levelrewards(member, userdata.getlevel(member.id))
                        if member.voice.mute or member.voice.self_mute:
                            userdata.setlastvcafk(member.id, True)
                        else:
                            userdata.setlastvcafk(member.id, False)
                    else:
                        userdata.addxp(member.id, random.randint(config.get("xp", {}).get("reaction", {}).get("min", 25), config.get("xp", {}).get("reaction", {}).get("max", 25)))
                        if userdata.getxp(member.id) >= self.levelrequirement(userdata.getlevel(member.id)) and len(channel.members) >= config.get("xp", {}).get("voice", {}).get("enabled", False).get("minimum-members", 0):
                            userdata.addlevel(member.id, 1)
                            userdata.setxp(member.id, 0)
                            await self.levelmessage(channel, member)
                            await self.levelrewards(member, userdata.getlevel(member.id))

    @group.command(name="rank", description="get yours or another members XP and level")
    async def rank(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer(ephemeral=True)
        if not member:
            member = interaction.user
        formattedname = ''.join([member.display_name, "'"]) if member.display_name.endswith("s") else ''.join([member.display_name, "'s"])
        embed = discord.Embed(title=f"{formattedname} rank card", color=discord.Color.purple())
        level = userdata.getlevel(member.id)
        xp = userdata.getxp(member.id)
        required = self.levelrequirement(level)
        progress_ratio = min(max(xp / required, 0), 1) if required else 0
        filled = int(progress_ratio * 10)
        empty = 10 - filled
        bar = ":purple_square:" * filled + ":black_large_square:" * empty
        percent = int(progress_ratio * 100)
        embed.add_field(
            name=f"lvl {level} - {xp}/{required}",
            value=f"{bar} `{percent}%`",
            inline=False
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @group.command(name="leaderboard", description="get a leaderboard of the server's levels")
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if not config.get("leaderboard", {}).get("enabled", True):
            await interaction.followup.send("the leaderboard feature is disabled :<", ephemeral=True)
            return

        entries = config.get("leaderboard", {}).get("entries", 10)
        top_users = userdata.xptop(entries)
        embed = discord.Embed(title="Leaderboard", color=discord.Color.purple())

        for index, user_id in enumerate(top_users, start=1):
            try:
                member = await self.bot.fetch_user(user_id)
            except discord.NotFound:
                continue

            level = userdata.getlevel(user_id)
            xp = userdata.getxp(user_id)
            required = self.levelrequirement(level)

            progress_ratio = min(max(xp / required, 0), 1) if required else 0
            filled = int(progress_ratio * 10)
            empty = 10 - filled
            bar = ":purple_square:" * filled + ":black_large_square:" * empty
            percent = int(progress_ratio * 100)

            embed.add_field(
                name=f"#{index} - [lvl {level}] {member.name}",
                value=f"{bar} `{percent}%`",
                inline=False
            )

        await interaction.followup.send(embed=embed)

    # Config reload
    @group.command(name="reload", description="reload the level configuration")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("somebody's got a lock on the levelling config. wait a sec, and try again", ephemeral=True)
            return
        self.lock = True
        global config
        if not os.path.isfile(config_path):
            await interaction.followup.send("a config.json for levelling was not found!! please read the README for setup instructions", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        print(f"{interaction.user.name} ({interaction.user.id}) reloaded the levelling configuration.")
        self.start_vccheck_loop()
        await interaction.followup.send("levelling configuration reloaded successfully", ephemeral=True)
        self.lock = False
    
    @xpgroup.command(name="set", description="set a user's XP")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def xpset(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        amount = max(0, min(amount, self.levelrequirement(userdata.getlevel(member.id))-1))
        userdata.setxp(member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) set {member.name}'s ({member.id}) XP to {amount}.")
        await interaction.followup.send(f"set {member.mention}'s XP to {amount}\n-# this may have been capped to (next level requirement-1) or 0", ephemeral=True)

    @xpgroup.command(name="add", description="give a user XP")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def xpadd(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount <= 0:
            await interaction.followup.send("you cannot give <= 0 XP to someone")
            return
        amount = min(amount, self.levelrequirement(userdata.getlevel(member.id))-1)
        userdata.addxp(member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) gave {member.name} ({member.id}) {amount}XP.")
        await interaction.followup.send(f"gave {member.mention} {amount}XP\n-# this may have been capped to (next level requirement-1)", ephemeral=True)

    @xpgroup.command(name="take", description="take a user's XP")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def xptake(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount <= 0:
            await interaction.followup.send("you cannot take <= 0 XP from someone")
            return
        amount = min(amount, userdata.getxp(member.id))
        userdata.takexp(member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) took {amount}XP from {member.name} ({member.id})")
        await interaction.followup.send(f"took {amount}XP from {member.mention}\n-# This may have been capped to prevent them from going below 0", ephemeral=True)

    # Add XP subgroup to level group
    group.add_command(xpgroup)

    @levelgroup.command(name="set", description="set a user's level")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setlevel(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        max_level = config.get("xp", {}).get("formula", {}).get("max-level", 0)
        if max_level > 0:
            amount = min(amount, max_level)
        if amount <= 0:
            amount = 1
        userdata.setlevel(member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) set {member.name}'s ({member.id}) level to {amount}.")
        await interaction.followup.send(f"set {member.mention}'s level to {amount}\n-# this may have been capped to respect a minimum level of 1 or the level cap", ephemeral=True)

    @levelgroup.command(name="add", description="add to a user's level")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def addlevel(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount <= 0:
            await interaction.followup.send("you cannot give <= 0 levels to someone")
            return
        current_level = userdata.getlevel(member.id)
        max_level = config.get("xp", {}).get("formula", {}).get("max-level", 0)
        if max_level > 0:
            amount = min(amount, max(0, max_level - current_level))
        userdata.addlevel(member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) added {amount} levels to {member.name} ({member.id}).")
        await interaction.followup.send(f"added {amount} levels to {member.mention}\n-# this may have been capped to respect the level cap", ephemeral=True)

    @levelgroup.command(name="take", description="take levels from a user")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def takelevel(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount <= 0:
            await interaction.followup.send("you cannot take <= 0 levels from someone")
            return
        current_level = userdata.getlevel(member.id)
        if current_level - amount <= 0:
            amount = current_level-1
        userdata.takelevel(member.id, amount)
        print(f"{interaction.user.name} ({interaction.user.id}) took {amount} levels from {member.name} ({member.id}).")
        await interaction.followup.send(f"took {amount} levels from {member.mention}\n-# This may have been capped to respect a minimum level of 1", ephemeral=True)

    # Add level subgroup to level group
    group.add_command(levelgroup)

    # Message XP
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if config.get("xp", {}).get("message", {}).get("enabled", False):
            lastmessage = userdata.getlastmessage(message.author.id)
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
                userdata.addxp(message.author.id, xp_earned)
                userdata.setlastmessage(message.author.id, int(time.time()))
            levelreq = self.levelrequirement(userdata.getlevel(message.author.id))
            if userdata.getxp(message.author.id) >= levelreq:
                userdata.addlevel(message.author.id, 1)
                userdata.setxp(message.author.id, 0)
                await self.levelmessage(message.channel, message.author)
                await self.levelrewards(message.author, userdata.getlevel(message.author.id))

    # Reaction XP
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = await self.bot.fetch_user(payload.user_id)
        channel = await self.bot.fetch_channel(payload.channel_id)
        if user.bot:
            return
        if config.get("xp", {}).get("reaction", {}).get("enabled", False):
            lastmessage = userdata.getlastreaction(user.id)
            cooldown = config.get("xp", {}).get("reaction", {}).get("cooldown", 300)
            if lastmessage == 0 or int(time.time()) - lastmessage >= cooldown:
                xp_earned = random.randint(config.get("xp", {}).get("reaction", {}).get("min", 25),
                                           config.get("xp", {}).get("reaction", {}).get("max", 25))
                xp_earned = await self.xp_calc(xp_earned,
                                               [role.id for role in user.roles],
                                               channel.id)
                userdata.addxp(user.id, xp_earned)
                userdata.setlastreaction(user.id, int(time.time()))
            levelreq = self.levelrequirement(userdata.getlevel(user.id))
            if userdata.getxp(user.id) >= levelreq:
                userdata.addlevel(user.id, 1)
                userdata.setxp(user.id, 0)
                await self.levelmessage(channel, user)
                await self.levelrewards(user, userdata.getlevel(user.id))


async def setup(squishy) -> None:
    print("Loading levelling extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA config.json for levelling was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    await squishy.add_cog(LevellingCog(squishy))
    print("LevellingCog loaded")