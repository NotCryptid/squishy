import os
import json
import asyncio
import discord
from discord.ext import commands

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA config.json for welcome was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ordinal(self, n):
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return str(n) + suffix

    def replace_variables(self, text, member):
        values = {
            "user.at": member.name,
            "user.id": member.id,
            "user.display": member.display_name,
            "user.mention": member.mention,
            "user.avatar": member.display_avatar.url if member.display_avatar else f"https://cdn.discordapp.com/embed/avatars/{int(member.id) % 5}.png",
            "server.name": member.guild.name,
            "server.id": member.guild.id,
            "server.icon": member.guild.icon.url if member.guild.icon else "",
            "membercount": member.guild.member_count,
            "membercount.format": self.ordinal(member.guild.member_count),
            "time": int(discord.utils.utcnow().timestamp()),
            "time.iso": discord.utils.utcnow().isoformat(),
        }
        for key, value in values.items():
            text = text.replace("{" + key + "}", str(value))
        return text

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        channel = member.guild.get_channel(config.get("welcome", {}).get("channel-id", 0))
        if config.get("welcome", {}).get("channel", False) and channel and isinstance(channel, discord.TextChannel):
            message = self.replace_variables(config.get("welcome", {}).get("content", ""), member) if config.get("welcome", {}).get("content") else ""
            embeds = [discord.Embed.from_dict(embed) for embed in json.loads(self.replace_variables(json.dumps(config["welcome"]["embeds"]), member))] if "embeds" in config.get("welcome", {}) else None
            await channel.send(message, embeds=embeds)
        else:
            print(f"Welcome channel not found or not a text channel in {member.guild.name} ({member.guild.id})")
        if config.get("welcome", {}).get("dm", False):
            try:
                message = self.replace_variables(config.get("welcome", {}).get("dm", {}).get("content", ""), member) if config.get("welcome", {}).get("dm", {}).get("content") else ""
                embeds = [discord.Embed.from_dict(embed) for embed in json.loads(self.replace_variables(json.dumps(config["welcome"]["dm"]["embeds"]), member))] if "embeds" in config.get("welcome", {}).get("dm", {}) else None
                await member.send(message, embeds=embeds)
            except discord.Forbidden:
                print(f"Could not send DM to {member.name} ({member.id})")

class GoodbyeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ordinal(self, n):
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return str(n) + suffix

    def replace_variables(self, text, member):
        values = {
            "user.at": member.name,
            "user.id": member.id,
            "user.display": member.display_name,
            "user.mention": member.mention,
            "user.avatar": member.display_avatar.url if member.display_avatar else f"https://cdn.discordapp.com/embed/avatars/{int(member.id) % 5}.png",
            "server.name": member.guild.name,
            "server.id": member.guild.id,
            "server.icon": member.guild.icon.url if member.guild.icon else "",
            "membercount": member.guild.member_count,
            "membercount.format": self.ordinal(member.guild.member_count),
            "time": int(discord.utils.utcnow().timestamp()),
            "time.iso": discord.utils.utcnow().isoformat(),
        }
        for key, value in values.items():
            text = text.replace("{" + key + "}", str(value))
        return text

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await asyncio.sleep(1)
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target.id == member.id:
                return
        if member.bot:
            return
        channel = member.guild.get_channel(config.get("goodbye", {}).get("channel-id", 0))
        if config.get("goodbye", {}).get("channel", False) and channel and isinstance(channel, discord.TextChannel):
            message = self.replace_variables(config.get("goodbye", {}).get("content", ""), member) if config.get("goodbye", {}).get("content") else ""
            embeds = [discord.Embed.from_dict(embed) for embed in json.loads(self.replace_variables(json.dumps(config["goodbye"]["embeds"]), member))] if "embeds" in config.get("goodbye", {}) else None
            await channel.send(message, embeds=embeds)
        else:
            print(f"Goodbye channel not found or not a text channel in {member.guild.name} ({member.guild.id})")

class BannedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ordinal(self, n):
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return str(n) + suffix

    def replace_variables(self, text, member):
        values = {
            "user.at": member.name,
            "user.id": member.id,
            "user.display": member.display_name,
            "user.mention": member.mention,
            "user.avatar": member.display_avatar.url if member.display_avatar else f"https://cdn.discordapp.com/embed/avatars/{int(member.id) % 5}.png",
            "server.name": member.guild.name,
            "server.id": member.guild.id,
            "server.icon": member.guild.icon.url if member.guild.icon else "",
            "membercount": member.guild.member_count,
            "membercount.format": self.ordinal(member.guild.member_count),
            "time": int(discord.utils.utcnow().timestamp()),
            "time.iso": discord.utils.utcnow().isoformat(),
        }
        for key, value in values.items():
            text = text.replace("{" + key + "}", str(value))
        return text

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if user.bot:
            return
        channel = user.guild.get_channel(config.get("banned", {}).get("channel-id", 0))
        if config.get("banned", {}).get("channel", False) and channel and isinstance(channel, discord.TextChannel):
            message = self.replace_variables(config.get("banned", {}).get("content", ""), user) if config.get("banned", {}).get("content") else ""
            embeds = [discord.Embed.from_dict(embed) for embed in json.loads(self.replace_variables(json.dumps(config["banned"]["embeds"]), user))] if "embeds" in config.get("banned", {}) else None
            await channel.send(message, embeds=embeds)
        else:
            print(f"Banned channel not found or not a text channel in {user.guild.name} ({user.guild.id})")

async def setup(squishy) -> None:
    print("Loading welcome extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA config.json for welcome was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    if config.get("welcome", {}).get("channel", False) or config.get("welcome", {}).get("dm", False):
        await squishy.add_cog(WelcomeCog(squishy))
        print("WelcomeCog loaded")
    if config.get("goodbye", {}).get("channel", False):
        await squishy.add_cog(GoodbyeCog(squishy))
        print("GoodbyeCog loaded")
    if config.get("banned", {}).get("channel", False):
        await squishy.add_cog(BannedCog(squishy))
        print("BannedCog loaded")