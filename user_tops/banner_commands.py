import disnake
from disnake.ext import commands

class BannerView(disnake.ui.View):
    def __init__(self, user: disnake.User):
        super().__init__()
        self.user = user

    @disnake.ui.button(label="Серверный баннер", style=disnake.ButtonStyle.primary, custom_id="server_banner")
    async def server_banner_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        # Здесь не нужно вызывать defer(), так как это будет обрабатываться как кнопка
        member = interaction.guild.get_member(self.user.id)
        if member and member.banner:
            banner_url = member.banner.url
            description = "Это баннер пользователя на сервере."
        else:
            banner_url = None
            description = "У пользователя нет серверного баннера." if not self.user.banner else "Показан глобальный баннер."

        embed = disnake.Embed(
            title=f"Баннер пользователя {self.user.name}",
            description=description,
        )
        if banner_url:
            embed.set_image(url=banner_url)

        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="Глобальный баннер", style=disnake.ButtonStyle.primary, custom_id="global_banner")
    async def global_banner_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        # Здесь не нужно вызывать defer(), так как это будет обрабатываться как кнопка
        banner_url = self.user.banner.url if self.user.banner else None
        description = "Это глобальный баннер пользователя." if banner_url else "У пользователя нет глобального баннера."

        embed = disnake.Embed(
            title=f"Баннер пользователя {self.user.name}",
            description=description,
        )
        if banner_url:
            embed.set_image(url=banner_url)

        await interaction.response.edit_message(embed=embed, view=self)

def setup_banner_commands(bot: commands.Bot):
    @bot.slash_command(name='banner', description='Показать баннер пользователя.')
    async def banner(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.User = None):
        await inter.response.defer()  # Предварительный ответ для предотвращения тайм-аутов

        user = пользователь or inter.author

        # Начальная установка - показывать глобальный баннер
        banner_url = user.banner.url if user.banner else None
        description = "Это глобальный баннер пользователя." if banner_url else "У пользователя нет глобального баннера."

        embed = disnake.Embed(
            title=f"Баннер пользователя {user.name}",
            description=description,
        )
        if banner_url:
            embed.set_image(url=banner_url)

        view = BannerView(user=user)
        await inter.edit_original_response(embed=embed, view=view)