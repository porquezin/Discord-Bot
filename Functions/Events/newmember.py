import discord
import datetime
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        role_name = "Member"
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role:
            await member.add_roles(role)
        
        channel_id = 1180979666518016061
        channel = self.client.get_channel(channel_id)
        
        if channel:
            embed = discord.Embed(
                title="Seja Bem-Vindo!",
                timestamp=datetime.datetime.now(),
                description=f"Seja bem-vindo ao servidor, {member.mention}!\n\nNão se esqueça de visitar as regras em <#1180977110135885914>.",
                color=discord.Color.dark_purple()
            )
            await channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Welcome(client))
