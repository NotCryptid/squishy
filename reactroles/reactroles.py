import os
import json
import discord
from discord.ext import commands
from discord import app_commands

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA config.json for reactroles was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

class ReactrolesCog(commands.Cog):
    lock = False

    group = app_commands.Group(name="reactroles", description="Manage lines")

    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.group, guild=discord.Object(id=self.bot.server))

    @group.command(name="reload", description="reload the reactroles configuration")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("somebody's got a lock on the reactroles config. wait a sec, and try againw", ephemeral=True)
            return
        self.lock = True
        global config
        if not os.path.isfile(config_path):
            await interaction.response.send("a config.json for reactroles was not found!! please read the README for setup instructions", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        await self._sync_reactroles()
        print(f"{interaction.user.name} ({interaction.user.id}) reloaded the reactroles configuration.")
        await interaction.followup.send("reactroles configuration reloaded successfully", ephemeral=True)
        self.lock = False

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if str(payload.message_id) not in config:
            return
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return
        emoji_name = payload.emoji.name
        role_id = config[str(payload.message_id)].get(emoji_name)
        if role_id is None:
            return
        role = guild.get_role(role_id)
        if role is not None:
            await member.add_roles(role, reason="React role added")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if str(payload.message_id) not in config:
            return
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        member = guild.get_member(payload.user_id)
        if member is None:
            return
        emoji_name = payload.emoji.name
        role_id = config[str(payload.message_id)].get(emoji_name)
        if role_id is None:
            return
        role = guild.get_role(role_id)
        if role is not None:
            await member.remove_roles(role, reason="React role removed")

    async def _sync_reactroles(self):
        await self.bot.wait_until_ready()
        for message_id, emoji_role_map in config.items():
            channel_id = emoji_role_map.get("channel")
            if channel_id:
                channel = self.bot.get_channel(channel_id)
            else:
                channel = discord.utils.get(self.bot.get_all_channels(), id=int(message_id))
            if channel is None:
                continue
            try:
                message = await channel.fetch_message(int(message_id))
            except (discord.NotFound, discord.Forbidden):
                continue
            # Add preset reactions
            for emoji_key in emoji_role_map.keys():
                if emoji_key == "channel":
                    continue
                try:
                    await message.add_reaction(emoji_key)
                except discord.HTTPException as e:
                    print(f"Failed to add reaction {emoji_key} on message {message.id}: {e}")

            # Retroactive react role assignment should the bot have been offline
            for reaction in message.reactions:
                emoji_key = str(reaction.emoji)
                if emoji_key not in emoji_role_map:
                    continue
                role_id = emoji_role_map[emoji_key]
                role = message.guild.get_role(role_id)
                if role is None:
                    continue
                async for user in reaction.users():
                    if user.bot:
                        continue
                    member = message.guild.get_member(user.id)
                    if member and role not in member.roles:
                        try:
                            await member.add_roles(role, reason="Retroactive react role assignment")
                        except discord.Forbidden as e:
                            print(f"Failed to add role {role.name} to {member.display_name}: {e}")

    async def cog_load(self):
        await self._sync_reactroles()

async def setup(squishy) -> None:
    print("Loading reactroles extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA config.json for reactroles was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    await squishy.add_cog(ReactrolesCog(squishy))
    print("ReactrolesCog loaded")