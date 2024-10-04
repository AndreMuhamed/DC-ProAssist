import disnake
from disnake.ext import commands
from disnake.ui import Button, View
import json
import os
from Translator.stay import translations  # Импортируем переводы

class StayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'admin/servers_data.json'
        self.load_data()
        self.user_languages = {}  # Хранение выбора языка для каждого пользователя

    def load_data(self):
        """Загружает данные о серверах из JSON файла."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.servers_data = json.load(f)
        else:
            self.servers_data = {}

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        """Обрабатывает событие присоединения бота к новому серверу.""" 
        server_id = str(guild.id)

        if server_id in self.servers_data:
            await self.send_staying_message(guild)

    async def send_staying_message(self, guild: disnake.Guild):
        """Отправляет сообщение о том, что бот остается на сервере."""
        # Получаем системный канал
        system_channel = guild.system_channel

        if system_channel and system_channel.permissions_for(guild.me).send_messages:
            # Отправляем сообщение в системный канал
            channel = system_channel
        else:
            # Если системный канал не настроен, выбираем первый доступный текстовый канал
            channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
        
        if channel:
            embed = disnake.Embed(
                title=translations["ru"]["stay_message_title"],
                description=translations["ru"]["stay_message_description"].format(server_name=guild.name),
            )

            # Добавляем GIF в эмбед
            gif_url = "https://media.discordapp.net/attachments/1089651879836913817/1291372224581861386/5f7559606a38ee11.gif?"
            embed.set_image(url=gif_url)  # Добавление GIF

            # Кнопки для выбора языка
            view = View()
            button_ru = Button(label="Русский", style=disnake.ButtonStyle.danger, custom_id="select_ru")
            button_uk = Button(label="Українська", style=disnake.ButtonStyle.danger, custom_id="select_uk")
            button_en = Button(label="English", style=disnake.ButtonStyle.danger, custom_id="select_en")

            view.add_item(button_ru)
            view.add_item(button_uk)
            view.add_item(button_en)

            # Кнопка с постоянной ссылкой на проекты создателя
            button_projects = Button(label=translations["ru"]["projects_button"], 
                                     url="https://andremuhamed.nexcord.pro/multilink/creator/torex", 
                                     style=disnake.ButtonStyle.link)
            view.add_item(button_projects)

            await channel.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.MessageInteraction):
        """Обработчик нажатий на кнопки для выбора языка."""
        if interaction.component.custom_id in ["select_ru", "select_uk", "select_en"]:
            user_id = str(interaction.user.id)
            user_language = interaction.component.custom_id.split("_")[-1]
            self.user_languages[user_id] = user_language  # Сохраняем язык пользователя

            # Обновляем текст сообщения в зависимости от выбранного языка
            title = translations[user_language]["stay_message_title"]
            description = translations[user_language]["stay_message_description"].format(server_name=interaction.guild.name)

            # Обновляем кнопки для дальнейшего выбора языка
            view = View()
            button_ru = Button(label="Русский", style=disnake.ButtonStyle.danger, custom_id="select_ru")
            button_uk = Button(label="Українська", style=disnake.ButtonStyle.danger, custom_id="select_uk")
            button_en = Button(label="English", style=disnake.ButtonStyle.danger, custom_id="select_en")

            view.add_item(button_ru)
            view.add_item(button_uk)
            view.add_item(button_en)

            # Обновляем кнопку с постоянной ссылкой на проекты создателя
            button_projects = Button(label=translations[user_language]["projects_button"], 
                                     url="https://andremuhamed.nexcord.pro/multilink/creator/torex", 
                                     style=disnake.ButtonStyle.link)
            view.add_item(button_projects)

            embed = disnake.Embed(title=title, description=description)

            # Добавляем GIF в обновленный эмбед
            gif_url = "https://media.discordapp.net/attachments/1089651879836913817/1291372224581861386/5f7559606a38ee11.gif?"
            embed.set_image(url=gif_url)  # Используем тот же URL для GIF
            await interaction.response.edit_message(embed=embed, view=view)

def setup(bot):
    bot.add_cog(StayCommand(bot))



