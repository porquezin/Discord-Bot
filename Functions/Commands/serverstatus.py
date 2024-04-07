import discord
from discord import app_commands
from discord.ext import commands

from utils.sysinfo import SystemInfo

class serverStatus(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.system_info = SystemInfo()

    @app_commands.command(name="server_status", description="Verifica o status e informações do bot.",)
    async def server_status(self, ctx: discord.Interaction):
        await ctx.response.defer()
        
        embed = discord.Embed(title="Status do Servidor", description="", color=discord.Color.dark_magenta())
        embed.set_thumbnail(url="https://www.shareicon.net/data/2015/09/14/100876_linux_512x512.png")

        embed.add_field(name="Sistema Operacional", value=self.system_info.distro_linux_name if self.system_info.platform != "Windows" else self.system_info.platform, inline=True)
        embed.add_field(name="", value="", inline=False)

        embed.add_field(name="Uso de CPU", value=self.system_info.cpu_usage, inline=True)
        embed.add_field(name="Uso de Memória", value=f"{self.system_info.info_memory}", inline=True)
        embed.add_field(name="", value="", inline=False)
        
        embed.add_field(name="Processador", value=self.system_info.cpu_info[1], inline=True)
        embed.add_field(name="", value="", inline=False)  
        
        embed.add_field(name="Arquitetura", value=self.system_info.cpu_info[0], inline=True)
        embed.add_field(name="Núcleos", value=self.system_info.cpu_info[2], inline=True)
        embed.add_field(name="Threads", value=self.system_info.cpu_info[3], inline=True)
        embed.add_field(name="", value="", inline=False)  
        embed.add_field(name="Virtualizado", value=self.system_info.cpu_info[4], inline=True)

        await ctx.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(serverStatus(client))