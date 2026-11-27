import discord
from discord.ext import commands
import random
import json
import os

TOKEN = "REPLACE_TOKEN"
DATA_FILE = "characters.json"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(campaigns, file, indent=4)


campaigns = load_data()


async def success(ctx):
    try:
        await ctx.message.add_reaction("✅")
    except:
        pass


async def failure(ctx):
    try:
        await ctx.message.add_reaction("❌")
    except:
        pass


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def roll(ctx, minimum: int, maximum: int, modifier: int = 0):

    if minimum > maximum:
        await failure(ctx)
        await ctx.send("Minimum cannot be greater than maximum.")
        return

    base_roll = random.randint(minimum, maximum)
    final_roll = base_roll + modifier

    await success(ctx)

    await ctx.send(
        f"Base Roll: {base_roll}\n"
        f"Modifier: {modifier}\n"
        f"Final Roll: {final_roll}"
    )


@bot.command()
async def newcampaign(ctx, *, campaign_name):

    if campaign_name in campaigns:
        await failure(ctx)
        await ctx.send("Campaign already exists.")
        return

    campaigns[campaign_name] = {}

    save_data()

    await success(ctx)
    await ctx.send(f"Campaign '{campaign_name}' created.")


@bot.command()
async def deletecampaign(ctx, *, campaign_name):

    if campaign_name not in campaigns:
        await failure(ctx)
        await ctx.send("Campaign not found.")
        return

    del campaigns[campaign_name]

    save_data()

    await success(ctx)
    await ctx.send(f"Deleted campaign '{campaign_name}'.")


@bot.command()
async def campaignslist(ctx):

    if len(campaigns) == 0:
        await failure(ctx)
        await ctx.send("No campaigns found.")
        return

    msg = "**Campaigns**\n"

    for campaign_name in campaigns:
        msg += f"• {campaign_name}\n"

    await success(ctx)
    await ctx.send(msg)


@bot.command()
async def addcharacter(ctx, campaign, name, char_class, level: int):

    if campaign not in campaigns:
        await failure(ctx)
        await ctx.send("Campaign not found.")
        return

    campaigns[campaign][name] = {
        "class": char_class,
        "level": level,
        "race": "Unknown",
        "notes": "No notes",
        "image": ""
    }

    save_data()

    await success(ctx)
    await ctx.send(f"{name} added to {campaign}.")


@bot.command()
async def deletecharacter(ctx, campaign, name):

    if campaign not in campaigns:
        await failure(ctx)
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
        await failure(ctx)
        await ctx.send("Character not found.")
        return

    del campaigns[campaign][name]

    save_data()

    await success(ctx)
    await ctx.send(f"{name} deleted.")


@bot.command()
async def setrace(ctx, campaign, name, *, race):

    if campaign not in campaigns:
        await failure(ctx)
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
        await failure(ctx)
        await ctx.send("Character not found.")
        return

    campaigns[campaign][name]["race"] = race

    save_data()

    await success(ctx)
    await ctx.send("Race updated.")


@bot.command()
async def note(ctx, campaign, name, *, text):

    if campaign not in campaigns:
        await failure(ctx)
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
        await failure(ctx)
        await ctx.send("Character not found.")
        return

    campaigns[campaign][name]["notes"] = text

    save_data()

    await success(ctx)
    await ctx.send("Notes updated.")


@bot.command()
async def getnotes(ctx, campaign, name):

    if campaign not in campaigns:
        await failure(ctx)
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
        await failure(ctx)
        await ctx.send("Character not found.")
        return

    await success(ctx)

    await ctx.send(
        f"Notes for {name}:\n{campaigns[campaign][name]['notes']}"
    )


@bot.command()
async def image(ctx, campaign, name, *, url):

    if campaign not in campaigns:
        await failure(ctx)
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
        await failure(ctx)
        await ctx.send("Character not found.")
        return

    campaigns[campaign][name]["image"] = url

    save_data()

    await success(ctx)
    await ctx.send("Image updated.")


@bot.command()
async def character(ctx, campaign, name):

    if campaign not in campaigns:
        await failure(ctx)
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
        await failure(ctx)
        await ctx.send("Character not found.")
        return

    char = campaigns[campaign][name]

    embed = discord.Embed(
        title=name,
        description=f"Level {char['level']} {char['class']}",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Race",
        value=char["race"],
        inline=True
    )

    embed.add_field(
        name="Campaign",
        value=campaign,
        inline=True
    )

    embed.add_field(
        name="Notes",
        value=char["notes"],
        inline=False
    )

    if char["image"] != "":
        embed.set_thumbnail(url=char["image"])

    await success(ctx)
    await ctx.send(embed=embed)


@bot.command()
async def campaign(ctx, *, campaign_name):

    if campaign_name not in campaigns:
        await failure(ctx)
        await ctx.send("Campaign not found.")
        return

    embed = discord.Embed(
        title=f"{campaign_name} Characters",
        color=discord.Color.green()
    )

    if len(campaigns[campaign_name]) == 0:
        embed.description = "No characters."

    for character_name, char in campaigns[campaign_name].items():

        embed.add_field(
            name=character_name,
            value=f"{char['class']} Lv.{char['level']}",
            inline=False
        )

    await success(ctx)
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):

    await success(ctx)

    await ctx.send("""
**DICE**
!roll <min> <max> <modifier>

**CAMPAIGNS**
!newcampaign <name>
!campaignslist
!campaign <campaignName>
!deletecampaign <campaignName>

**CHARACTERS**
!addcharacter <campaign> <name> <class> <level>
!character <campaign> <name>
!deletecharacter <campaign> <name>

**CUSTOMIZATION**
!setrace <campaign> <name> <race>
!note <campaign> <name> <text>
!getnotes <campaign> <name>
!image <campaign> <name> <imageURL>

**IMPORTANT**
Campaign names with spaces must be wrapped in quotes.

Example:
!campaign "Curse of Strahd"

!character "Curse of Strahd" Thorin

**NOTE**
For image URLs, catbox.moe is recommended.
""")


bot.run(TOKEN)
