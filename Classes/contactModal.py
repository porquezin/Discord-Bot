import discord
import datetime

class ContactModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Contact", *args, **kwargs)

    subject = discord.ui.TextInput(
        label="Assunto:",
        style=discord.TextStyle.short,
        required=True
    )

    message = discord.ui.TextInput(
        label="Mensagem:",
        style=discord.TextStyle.long,
        required=True,
        max_length=512
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Contact",
            timestamp=datetime.datetime.now(),
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name=f"{self.subject.value}:", value=f"{self.message.value}\n\nby: {interaction.user.mention}")

        contact_channel_id = 1221193003872551056
        channel = interaction.guild.get_channel(contact_channel_id)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("Registrado com sucesso!", ephemeral=True)
        else:
            await interaction.response.send_message("Erro ao encontrar o canal.", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Não registrado. Tente novamente mais tarde!", ephemeral=True)
