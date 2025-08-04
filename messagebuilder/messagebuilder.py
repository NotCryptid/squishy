import os
import json
import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands

class MessagebuilderCog(commands.Cog):
    lock = False

    group = app_commands.Group(name="messagebuilder", description="Manage lines")

    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.group, guild=discord.Object(id=self.bot.server))
        self.stored_embeds = {}
        self.purge_embeds_task.start()

    @tasks.loop(minutes=30)
    async def purge_embeds_task(self):
        self.stored_embeds.clear()
        print("Stored embeds have been purged.")

    @purge_embeds_task.before_loop
    async def before_purge(self):
        await self.bot.wait_until_ready()

    # Command to add an embed from JSON
    @group.command(name="addembed", description="Add an embed from JSON")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def add_embed(self, interaction: discord.Interaction, json_data: str):
        await interaction.response.defer(ephemeral=True)
        try:
            embed_dict = json.loads(json_data)
            embed = discord.Embed.from_dict(embed_dict)
        except (json.JSONDecodeError, TypeError) as e:
            await interaction.followup.send(f"invalid JSON or embed format: {e}", ephemeral=True)
            return

        # Create a unique ID (simple incremental or UUID)
        embed_id = str(len(self.stored_embeds) + 1)
        self.stored_embeds[embed_id] = embed
        await interaction.followup.send(f"embed stored with ID: `{embed_id}`", ephemeral=True)

    # Command to send a stored embed by ID in the current channel
    @group.command(name="sendembed", description="Send a stored embed by its ID")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def send_embed(self, interaction: discord.Interaction, embed_id: str):
        await interaction.response.defer(ephemeral=True)
        embed = self.stored_embeds.get(embed_id)
        if not embed:
            await interaction.followup.send("Embed ID not found.", ephemeral=True)
            return
        await interaction.channel.send(embed=embed)
        await interaction.followup.send("sent!", ephemeral=True)
    
    

async def setup(squishy) -> None:
    print("Loading messagebuilder extension...")
    await squishy.add_cog(MessagebuilderCog(squishy))
    print("MessagebuilderCog loaded")