import os
import json
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from datahandler import Economy

userdata = Economy()

config_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.isfile(config_path):
    print("\033[31;1mA config.json for economy was not found!!\033[0m Please read the README for setup instructions.")

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

class EconomyCog(commands.Cog):
    lock = False

    group = app_commands.Group(name="economy", description="interact with the server's economy")
    shopgroup = app_commands.Group(name="shop", description="browse and buy from the shop")

    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.group, guild=discord.Object(id=self.bot.server))

    def formatcurrency(self, amount):
        amount = str(amount)
        if config.get("currency-placement", 2) == 1:
            amount = ''.join([config.get("currency-symbol", "$"), amount])
        else:
            amount = ''.join([amount, config.get("currency-symbol", "$")])
        return(amount)

    @group.command(name="reload", description="reload the economy configuration")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.lock:
            await interaction.followup.send("somebody's got a lock on the economy config. wait a sec, and try again", ephemeral=True)
            return
        self.lock = True
        global config
        if not os.path.isfile(config_path):
            await interaction.response.send("a config.json for economy was not found!! please read the README for setup instructions", ephemeral=True)
            self.lock = False
            return
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        print(f"{interaction.user.name} ({interaction.user.id}) reloaded the economy configuration.")
        await interaction.followup.send("economy configuration reloaded successfully.", ephemeral=True)
        self.lock = False

    @group.command(name="give", description="give a member some money")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def give(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount <= 0:
            await interaction.followup.send(f"you cannot give <= 0 {config.get('currency-symbol', '$')} to someone")
            return
        if config.get("max-bal", 0) > 0:
            bal = userdata.getbal(member.id)
            amount = min(amount, max(0, config.get("max-bal") - bal))
        userdata.addbal(member.id, amount)
        await interaction.followup.send(f"gave {member.mention} {self.formatcurrency(amount)}\n-# this may have been capped to respect the max balance")

    @group.command(name="take", description="take some of a member's money")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def take(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount <= 0:
            await interaction.followup.send(f"you cannot take <= 0 {config.get('currency-symbol', '$')} from someone")
            return
        bal = userdata.getbal(member.id)
        if bal - amount == 0:
            amount = bal
        amount = min(amount, bal)
        userdata.takebal(member.id, amount)
        await interaction.followup.send(f"took {self.formatcurrency(amount)} from {member.mention}\n-# this may have been capped to prevent someone from going <0")

    @group.command(name="pay", description="send another member some money")
    async def pay(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await interaction.response.defer(ephemeral=True)
        if amount <= 0:
            await interaction.followup.send(f"you cannot send <= 0 {config.get('currency-symbol', '$')}")
            return
        bal = userdata.getbal(member.id)
        if config.get("max-bal", 0) > 0:        
            amount = min(amount, max(0, config.get("max-bal") - bal))
        if amount >= userdata.getbal(interaction.user.id):
            await interaction.followup.send(f"you don't have enough {config.get('currency-name', 'money')}")
            return
        userdata.addbal(member.id, amount)
        userdata.takebal(interaction.user.id, amount)
        await interaction.followup.send(f"sent {member.mention} {self.formatcurrency(amount)}\n-# this may have been capped to respect the max balance")
        await member.send(f"{interaction.user.mention} ({interaction.user.name}) sent you {self.formatcurrency(amount)}!")

    @group.command(name="balance", description="Check your balance")
    async def balance(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        bal = str(userdata.getbal(interaction.user.id))
        await interaction.followup.send(f"you have {self.formatcurrency(bal)}", ephemeral=True)

    @shopgroup.command(name="shop", description="browse items in the shop")
    async def shop(self, interaction: discord.Interaction, page: int = 1):
        await interaction.response.defer(ephemeral=True)

        shop_items = config.get("shop", {}).get("items", {})
        currency_symbol = config.get("currency-symbol", "$")

        item_ids = sorted(shop_items.keys(), key=lambda k: int(k))
        items_per_page = 5
        start = (page - 1) * items_per_page
        end = start + items_per_page
        selected_ids = item_ids[start:end]

        if not selected_ids:
            await interaction.followup.send("no items found on this page.", ephemeral=True)
            return

        embeds = []
        for item_id in selected_ids:
            item = shop_items[item_id]
            name = item.get("name", "unnamed")
            price = item.get("cost", 0)
            description = item.get("description", "no description.")

            embed = discord.Embed(
                title=name,
                description=f"{price} {currency_symbol}\n{description}",
                color=discord.Color.purple()
            )
            embed.set_footer(text=f"buy with /shop buy id:{item_id}!")
            embeds.append(embed)

        await interaction.followup.send(embeds=embeds, ephemeral=True)

    @shopgroup.command(name="buy", description="buy an item from the shop")
    async def buy(self, interaction: discord.Interaction, itemid: int, giftto: discord.Member = None):
        await interaction.response.defer(ephemeral=True)

        shop_items = config.get("shop", {}).get("items", {})
        item = shop_items.get(str(itemid))
        if not item:
            await interaction.followup.send("that item doesn't exist", ephemeral=True)
            return

        buyer_id = interaction.user.id
        recipient = giftto or interaction.user
        recipient_id = recipient.id

        repurchasable = item.get("repurchasable", False)
        purchases = userdata.getpurchase(recipient_id)
        if not repurchasable and itemid in purchases:
            await interaction.followup.send(f"{recipient.mention} already owns this item", ephemeral=True)
            return

        cost = item.get("cost", 0)
        if userdata.getbal(buyer_id) < cost:
            await interaction.followup.send(f"you don't have enough {config.get('currency-name-plural', 'currency')} to buy this item", ephemeral=True)
            return

        rewards = item.get("rewards", [])
        for reward in rewards:
            rtype = reward.get("type", None)
            value1 = reward.get("value1", None)
            value2 = reward.get("value2", None)

            if rtype == "role":
                role = interaction.guild.get_role(int(value1))
                if role and role not in recipient.roles:
                    await recipient.add_roles(role, reason="Shop purchase")
            elif rtype == "temprole":
                role = interaction.guild.get_role(int(value1))
                if role and role not in recipient.roles:
                    await recipient.add_roles(role, reason="Shop temporary role")
                    async def remover():
                        await asyncio.sleep(int(value2))
                        await recipient.remove_roles(role, reason="Temporary role expired")
                    self.bot.loop.create_task(remover())
            elif rtype == "script":
                script_path = os.path.join(os.path.dirname(__file__), "..", "customs", "scripts", f"{value1}.py")
                if os.path.isfile(script_path):
                    namespace = {}
                    with open(script_path, "r", encoding="utf-8") as script_file:
                        exec(script_file.read(), namespace)
                    func = namespace.get("main")
                    if callable(func):
                        import inspect
                        params = inspect.signature(func).parameters
                        if len(params) == 2:
                            func(recipient_id, interaction.channel.id)
                        else:
                            func()
                    else:
                        exec(open(script_path, "r", encoding="utf-8").read(), {"recipient_id": recipient_id, "channel_id": interaction.channel.id})

        userdata.takebal(buyer_id, cost)
        userdata.addpurchase(recipient_id, itemid)

        await interaction.followup.send(f"succesfully bought **{item.get('name', 'an item')}**{''.join([' for ', recipient.mention] if recipient.mention != interaction.user else None)}!", ephemeral=True)

    group.add_command(shopgroup)

async def setup(squishy) -> None:
    print("Loading economy extension...")
    if not os.path.isfile(config_path):
        print("\033[31;1mA config.json for economy was not found!! The module will disable itself now.\033[0m Please read the README for setup instructions.")
        return
    await squishy.add_cog(EconomyCog(squishy))
    print("EconomyCog loaded")