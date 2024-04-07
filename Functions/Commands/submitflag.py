from discord import app_commands
from discord.ext import commands
import discord
import aiohttp
import datetime


class SubmitFlag(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.url_submit_flag = "http://localhost:5000/submit_flag"

    @app_commands.command(name="submit_flag", description="Valida uma flag.")
    async def submit(self, ctx: discord.Interaction, flag: str):
        user_id = ctx.user.id

        async with aiohttp.ClientSession() as session:
            payload = {"user_id": user_id, "flag": flag}
            async with session.post(self.url_submit_flag, json=payload) as response:
                
                if response.status == 201:
                    data = await response.json()
                    embed = discord.Embed(
                        title="✅ Flag correta!",
                        description=f"Você ganhou **{data['points_awarded']}** pontos!",
                        timestamp=datetime.datetime.now(),
                        color=discord.Color.brand_green())
                    embed.set_thumbnail(url=ctx.user.display_avatar.url)
                    embed.add_field(name="Total de Pontos", value=data['all_points'])
                    await ctx.response.send_message(embed=embed)
                
                elif response.status == 404:
                    await ctx.response.send_message("❌ Flag incorreta!", ephemeral=True)
                
                elif response.status == 400:
                    await ctx.response.send_message("❌ Flag já submetida!", ephemeral=True)
                
                else:
                    await ctx.response.send_message("⚠️ Houve um problema ao validar a flag. Entre em contado com a moderação.", ephemeral=True)


async def setup(client):
    await client.add_cog(SubmitFlag(client))
