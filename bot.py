import discord
from discord.ext import commands

import settings

client = commands.Bot(command_prefix=settings.PREFIX, help_command=None, intents=settings.INTENTS)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(name=settings.STATUS, type=discord.ActivityType.watching))
    for cog in settings.COGS:
        try:
            await client.load_extension(cog)
            print(f"Loaded cog {cog}.")
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(cog, exc))
    await client.tree.sync()
    print("Bot is ready!")

def start_bot(): 
    client.run(settings.TOKEN)

start_bot()