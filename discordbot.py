"""
D&D Campaign Manager Bot

This bot allows users to:
- Create and manage D&D campaigns
- Store character information
- Save notes and character portraits
- Roll dice with optional modifiers

Campaign data is stored in a JSON file so information
persists between bot restarts.
"""

import discord
from discord.ext import commands
import random
import json
import os

# The token is intentionally excluded from source control.
# Users must provide their own Discord bot token before running.
TOKEN = "REPLACE_WITH_YOUR_TOKEN"

# Character data is stored locally so campaigns survive
# bot restarts without requiring a database.
DATA_FILE = "characters.json"

intents = discord.Intents.default()
intents.message_content = True

# The default help command is disabled because the bot
# provides a help menu tailored to its D&D commands.
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


def load_data():
    """
    Attempt to load saved campaign data.

    If the file does not exist or becomes unreadable,
    the bot starts with an empty campaign list rather
    than failing to launch.
    """
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


def save_data():
    """
    Save all campaign data immediately after every change.

    Writing changes directly to disk minimizes the risk of
    losing character information if the bot unexpectedly stops.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(campaigns, file, indent=4)


campaigns = load_data()


async def success(ctx):
    """
    Reactions provide lightweight confirmation without
    cluttering channels with additional success messages.
    """
    try:
        await ctx.message.add_reaction("✅")
    except:
        pass


async def failure(ctx):
    """
    Error reactions make invalid commands easier to identify
    without requiring users to read multiple messages.
    """
    try:
        await ctx.message.add_reaction("❌")
    except:
        pass


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
