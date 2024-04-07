import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
STATUS = "Online"
PREFIX = "!!!"
INTENTS = discord.Intents.all()
COGS = ("Functions.Events.newmember",
        "Functions.Commands.contact",
        "Functions.Commands.serverstatus",
        "Functions.Commands.submitflag",
        "Functions.Commands.scoreboard"
        )
