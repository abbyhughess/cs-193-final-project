import discord
from discord.ext import commands
import random
import json
import os

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# REPLACE YOUR_TOKEN_HERE IN QUOTATION MARKS WITH YOUR OWN TOKEN
TOKEN = "YOUR_TOKEN_HERE"
# REPLACE YOUR_TOKEN_HERE IN QUOTATION MARKS WITH YOUR OWN TOKEN
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "characters.json"


# ------------------------
# SAVE / LOAD DATA
# ------------------------

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    return {}


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(campaigns, file, indent=4)


campaigns = load_data()


# ------------------------
# BOT READY
# ------------------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# ------------------------
# DICE COMMANDS
# ------------------------

@bot.command()
async def roll(ctx, minimum: int, maximum: int, modifier: int = 0):

    base_roll = random.randint(minimum, maximum)
    final_roll = base_roll + modifier

    await ctx.send(
        f"Base Roll: {base_roll}\n"
        f"Modifier: {modifier}\n"
        f"Final Roll: {final_roll}"
    )


@bot.command()
async def coinflip(ctx):

    result = random.choice(["Heads", "Tails"])

    await ctx.send(result)


# ------------------------
# CREATE CAMPAIGN
# ------------------------

@bot.command()
async def newcampaign(ctx, *, campaign_name):

    if campaign_name in campaigns:
        await ctx.send("Campaign already exists.")
        return

    campaigns[campaign_name] = {}

    save_data()

    await ctx.send(f"Campaign '{campaign_name}' created.")


# ------------------------
# LIST CAMPAIGNS
# ------------------------

@bot.command()
async def campaignslist(ctx):

    if len(campaigns) == 0:
        await ctx.send("No campaigns found.")
        return

    message = "**Campaigns**\n"

    for campaign in campaigns:
        message += f"• {campaign}\n"

    await ctx.send(message)


# ------------------------
# ADD CHARACTER
# ------------------------

@bot.command()
async def addcharacter(
    ctx,
    campaign,
    name,
    char_class,
    level: int
):

    if campaign not in campaigns:

        campaigns[campaign] = {}

    campaigns[campaign][name] = {
        "class": char_class,
        "level": level,
        "race": "Unknown",
        "notes": "No notes",
        "image": ""
    }

    save_data()

    await ctx.send(f"{name} added to {campaign}.")


# ------------------------
# UPDATE RACE
# ------------------------

@bot.command()
async def setrace(ctx, campaign, name, *, race):

    if campaign not in campaigns:
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
        await ctx.send("Character not found.")
        return

    campaigns[campaign][name]["race"] = race

    save_data()

    await ctx.send("Race updated.")


# ------------------------
# UPDATE NOTES
# ------------------------

@bot.command()
async def note(ctx, campaign, name, *, text):

    if campaign not in campaigns:
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
        await ctx.send("Character not found.")
        return

    campaigns[campaign][name]["notes"] = text

    save_data()

    await ctx.send("Notes updated.")


# ------------------------
# SET IMAGE URL
# ------------------------

@bot.command()
async def image(ctx, campaign, name, *, url):

    if campaign not in campaigns:
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
        await ctx.send("Character not found.")
        return

    campaigns[campaign][name]["image"] = url

    save_data()

    await ctx.send("Image updated.")


# ------------------------
# SHOW CHARACTER
# ------------------------

@bot.command()
async def character(ctx, campaign, name):

    if campaign not in campaigns:
        await ctx.send("Campaign not found.")
        return

    if name not in campaigns[campaign]:
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

    await ctx.send(embed=embed)


# ------------------------
# LIST CHARACTERS
# ------------------------

@bot.command()
async def campaign(ctx, *, campaign_name):

    if campaign_name not in campaigns:
        await ctx.send("Campaign not found.")
        return

    embed = discord.Embed(
        title=f"{campaign_name} Characters",
        color=discord.Color.green()
    )

    for character_name in campaigns[campaign_name]:

        char = campaigns[campaign_name][character_name]

        embed.add_field(
            name=character_name,
            value=f"{char['class']} Lv.{char['level']}",
            inline=False
        )

    await ctx.send(embed=embed)


# ------------------------
# HELP MENU
# ------------------------

@bot.command()
async def commandslist(ctx):

    await ctx.send("""
DICE
!roll min max modifier
!coinflip

CAMPAIGNS
!newcampaign name
!campaignslist
!campaign campaignname

CHARACTERS
!addcharacter campaign name class level
!character campaign name
!setrace campaign name race
!note campaign name text
!image campaign name imageURL
""")


bot.run(TOKEN)
