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
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


@bot.command()
async def bye(ctx):
    await ctx.send("Goodbye!")


@bot.command()
async def roll(ctx):
    number = random.randint(1, 6)
    await ctx.send(f"You rolled a {number}")


@bot.command()
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(result)


@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


@bot.command()
async def square(ctx, n: int):
    await ctx.send(n * n)


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
!ping
!hello
!bye
!roll
!coinflip
!add 5 10
!square 7
!userinfo
"""
    )


bot.run(TOKEN)
