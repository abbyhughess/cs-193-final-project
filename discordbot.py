import discord
from discord.ext import commands
import random

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
### PLEASE ENSURE YOU REPLACE THIS LINE OF CODE WITHIN THE QUOTATION MARKS
TOKEN = "YOUR_TOKEN_HERE"
### PLEASE ENSURE YOU REPLACE THIS LINE OF CODE WITHIN THE QUOTATION MARKS
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def roll(ctx, min: int, max: int, modifier: int):
    number = random.randint(min, max)
    rollint = number + modifier
    await ctx.send(f"You rolled a {rollint}. Your base roll was {number}")


@bot.command()
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(result)

@bot.command()
async def userinfo(ctx):
    await ctx.send(
        f"Username: {ctx.author.name}\n"
        f"User ID: {ctx.author.id}"
    )

@bot.command()
async def commandslist(ctx):
    await ctx.send(
        """
!roll
!coinflip
!userinfo
"""
    )


bot.run(TOKEN)
