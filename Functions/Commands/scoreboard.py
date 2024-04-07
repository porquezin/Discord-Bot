import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

class Scoreboard(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.url_users = "http://localhost:5000/scoreboard"

    @app_commands.command(name="scoreboard", description="Retorna o scoreboard atual.")
    async def scoreboard(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url_users) as response:
                if response.status == 200:
                    users = await response.json()
                    if not users:
                        await interaction.response.send_message("Ainda não há usuários no scoreboard.", ephemeral=True)
                        return

                    description_lines = []
                    for index, user in enumerate(users, start=1):
                        description_lines.append(f"{index} - {interaction.guild.get_member(user['user_id']).name} - Pontos: {user['points']}")

                    embed = discord.Embed(
                        title="🏆 Scoreboard",
                        description="\n".join(description_lines),
                        color=discord.Color.blue()
                    )
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("⚠️ Houve um problema ao buscar o scoreboard. Entre em contato com a moderação.", ephemeral=True)

async def setup(client):
    await client.add_cog(Scoreboard(client))
