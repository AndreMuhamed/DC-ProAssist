import disnake
from disnake.ext import commands

class AvatarView(disnake.ui.View):
    def __init__(self, user: disnake.User):
        super().__init__()
        self.user = user

    @disnake.ui.button(label="Глобальный аватар", style=disnake.ButtonStyle.primary, custom_id="global_avatar")
    async def global_avatar_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        avatar_url = self.user.avatar.url if self.user.avatar else self.user.default_avatar.url
        description = "Это глобальный аватар пользователя."

        embed = disnake.Embed(
            title=f"Аватар — {self.user.name}",
            description=description,
        )
        embed.set_image(url=avatar_url)

        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="Серверный аватар", style=disnake.ButtonStyle.primary, custom_id="server_avatar")
    async def server_avatar_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        member = interaction.guild.get_member(self.user.id)
        if member and member.display_avatar:
            avatar_url = member.display_avatar.url
            description = "Это серверный аватар пользователя."
        else:
            avatar_url = self.user.display_avatar.url
            description = "У пользователя нет серверного аватара. Показан глобальный аватар."

        embed = disnake.Embed(
            title=f"Аватар — {self.user.name}",
            description=description,
        )
        embed.set_image(url=avatar_url)

        await interaction.response.edit_message(embed=embed, view=self)

def setup_avatar_commands(bot: commands.Bot):
    @bot.slash_command(name='avatar', description='Показать аватар пользователя.')
    async def avatar(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.User = None):
        user = пользователь or inter.author

        # Начальная установка - показывать серверный аватар, если он есть
        member = inter.guild.get_member(user.id) if inter.guild else None
        if member and member.display_avatar:
            avatar_url = member.display_avatar.url
            description = "Это серверный аватар пользователя."
        else:
            avatar_url = user.display_avatar.url
            description = "У пользователя нет серверного аватара. Показан глобальный аватар."

        embed = disnake.Embed(
            title=f"Аватар — {user.name}",
            description=description,
        )
        embed.set_image(url=avatar_url)

        view = AvatarView(user=user)
        await inter.response.send_message(embed=embed, view=view)
