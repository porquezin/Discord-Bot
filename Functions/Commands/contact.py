import discord
from discord import app_commands
from discord.ext import commands

from Classes.contactModal import ContactModal


class Contact(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="contact", description="Entra em contato com um moderador.",)
    async def contact(self, interaction: discord.Interaction):
        contact_modal = ContactModal()
        await interaction.response.send_modal(contact_modal)

async def setup(client):
    await client.add_cog(Contact(client))