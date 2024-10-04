import disnake     
from disnake.ext import commands
from disnake.ui import Button, View
import json
import os
import asyncio
from Translator.leave import translations  # Импортируем переводы

class LeaveCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'admin/servers_data.json'
        self.load_data()
        self.goodbye_message_id = {}  # Хранение ID сообщения о прощании

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

        if server_id not in self.servers_data:
            await self.send_goodbye_message(guild)

    async def send_goodbye_message(self, guild: disnake.Guild):
        """Отправляет сообщение о том, что бот уходит с сервера."""
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = disnake.Embed(
                    title=translations["ru"]["bot_leaving_title"],
                    description=translations["ru"]["bot_leaving_description"].format(server_name=guild.name),
                )

                # Пример URL GIF, замените на ваш
                gif_url = "https://media.discordapp.net/attachments/1089651879836913817/1291372224581861386/5f7559606a38ee11.gif?"  # Замените это на ваш URL
                embed.set_image(url=gif_url)  # Добавление GIF в эмбед

                # Добавляем новый подпункт для доступа к продавцам
                embed.add_field(
                    name=translations["ru"]["seller_link_title"],
                    value="<@768782555171782667>, <@787093771115692062>",
                    inline=False
                )

                # Кнопки для выбора языка
                view_language = View()
                button_ru = Button(label="Русский", style=disnake.ButtonStyle.danger, custom_id="select_ru")
                button_uk = Button(label="Українська", style=disnake.ButtonStyle.danger, custom_id="select_uk")
                button_en = Button(label="English", style=disnake.ButtonStyle.danger, custom_id="select_en")

                view_language.add_item(button_ru)
                view_language.add_item(button_uk)
                view_language.add_item(button_en)

                # Кнопка со ссылкой на проекты создателя (постоянный URL)
                project_url = "https://andremuhamed.nexcord.pro/multilink/creator/torex"  # Замените на URL проектов
                project_button = Button(label=translations["ru"]["creator_projects_label"], style=disnake.ButtonStyle.link, url=project_url)
                view_language.add_item(project_button)

                # Отправляем сообщение и сохраняем его ID
                message = await channel.send(embed=embed, view=view_language)
                self.goodbye_message_id[str(guild.id)] = message.id
                break

        # Ждем 2 минуты перед выходом с сервера
        await asyncio.sleep(120)  # 120 секунд = 2 минуты
        await guild.leave()

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.MessageInteraction):
        """Обработчик нажатий на кнопки для выбора языка."""
        if interaction.component.custom_id in ["select_ru", "select_uk", "select_en"]:
            user_language = interaction.component.custom_id.split("_")[-1]

            # Получаем переводы на выбранном языке
            title = translations[user_language]["bot_leaving_title"]
            description = translations[user_language]["bot_leaving_description"].format(server_name=interaction.guild.name)

            # Если сообщение о прощании было отправлено, редактируем его
            goodbye_message_id = self.goodbye_message_id.get(str(interaction.guild.id))
            if goodbye_message_id:
                goodbye_channel = interaction.channel
                goodbye_message = await goodbye_channel.fetch_message(goodbye_message_id)

                # Создаем новый эмбед с обновленным текстом и GIF
                goodbye_embed = disnake.Embed(title=title, description=description)
                gif_url = "https://media.discordapp.net/attachments/1089651879836913817/1291372224581861386/5f7559606a38ee11.gif?"  # Замените это на ваш URL
                goodbye_embed.set_image(url=gif_url)  # Добавление GIF в эмбед

                # Добавляем новый подпункт для доступа к продавцам
                goodbye_embed.add_field(
                    name=translations[user_language]["seller_link_title"],
                    value="<@768782555171782667>, <@787093771115692062>",
                    inline=False
                )

                # Создаем кнопки для выбора языка
                view_language = View()
                button_ru = Button(label="Русский", style=disnake.ButtonStyle.danger, custom_id="select_ru")
                button_uk = Button(label="Українська", style=disnake.ButtonStyle.danger, custom_id="select_uk")
                button_en = Button(label="English", style=disnake.ButtonStyle.danger, custom_id="select_en")

                view_language.add_item(button_ru)
                view_language.add_item(button_uk)
                view_language.add_item(button_en)

                # Создаем новую кнопку со ссылкой на проекты
                project_button = Button(label=translations[user_language]["creator_projects_label"], style=disnake.ButtonStyle.link, url="https://andremuhamed.nexcord.pro/multilink/creator/torex")

                view_language.add_item(project_button)  # Добавляем кнопку проектов

                # Обновляем вью для отправки
                await goodbye_message.edit(embed=goodbye_embed, view=view_language)

def setup(bot):
    bot.add_cog(LeaveCommand(bot))













