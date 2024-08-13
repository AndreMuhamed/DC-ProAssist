import disnake
from disnake.ext import commands
from disnake.ui import Button, View, Modal, TextInput
import os

class SuggestionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='suggest', description='Получить ссылку на приглашение бота и предложить идею.')
    async def suggest(self, inter: disnake.ApplicationCommandInteraction):
        """Создает сообщение с ссылкой на приглашение бота и кнопкой для подачи предложений."""
        
        # Создание ссылки на приглашение
        invite_link = disnake.utils.oauth_url(self.bot.user.id, permissions=disnake.Permissions(permissions=8))  # Измените разрешения при необходимости
        
        # Создание эмбеда с приглашением и кнопкой
        invite_embed = disnake.Embed(
            title="<:Stickerus3:1269746081504170124> Пригласите бота на свой сервер!",
            description=(
                f"Вот **ссылка**, по которой вы можете **пригласить** бота на ваш сервер: [ТУТ]({invite_link})\n\n"
                f"Спасибо, что **используете** нашего бота! Ваше **мнение** очень важно для нас."
            )
        )
        
        # Добавление аватарки бота
        bot_avatar_url = self.bot.user.display_avatar.url
        invite_embed.set_thumbnail(url=bot_avatar_url)

        # Создание кнопки
        suggestion_button = Button(label="Предложить идею", style=disnake.ButtonStyle.primary, custom_id="suggestion_button")
        view = View()
        view.add_item(suggestion_button)

        await inter.send(embed=invite_embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, inter: disnake.Interaction):
        if inter.type == disnake.InteractionType.component and inter.data.get('custom_id') == "suggestion_button":
            # Создание модального окна
            modal = SuggestionModal()
            await inter.response.send_modal(modal)

class SuggestionModal(Modal):
    def __init__(self):
        super().__init__(title="Предложение")

        self.add_item(TextInput(label="Ваша идея", placeholder="Введите вашу идею здесь", required=True))
        self.add_item(TextInput(label="Контактная информация", placeholder="Введите ваш контакт (например, Discord ID или email)", required=True))

    async def callback(self, interaction: disnake.Interaction):
        idea = self.children[0].value
        contact = self.children[1].value

        # Сохранение данных в текстовый файл
        with open('suggestions.txt', 'a') as f:
            f.write(f"Идея: {idea}\nКонтакт: {contact}\n\n")

        await interaction.response.send_message("Ваша идея была успешно отправлена!", ephemeral=True)

def setup(bot):
    bot.add_cog(SuggestionCommands(bot))


