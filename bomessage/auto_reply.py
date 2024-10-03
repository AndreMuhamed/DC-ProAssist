import disnake
from disnake.ui import View, Button
from admin.data_handler import update_last_sent, save_data
from Translator.auto import translations  # Импортируем переводы
import os  # Импортируем os для проверки наличия файлов

# Создание класса для управления кнопками выбора языка
class LanguageSelector(View):
    def __init__(self, message: disnake.Message, data, user_id):
        super().__init__()  # Убрали тайм-аут
        self.message = message
        self.data = data
        self.user_id = user_id
        self.gif_mapping = {
            "ru": "assets/working_24_7.gif",
            "uk": "assets/working_24_7_uk.gif",  # Путь к гифке для украинского
            "en": "assets/working_24_7_en.gif",  # Путь к гифке для английского
        }
        self.saved_message_id = None  # Для сохранения идентификатора сообщения

        # Создание кнопок с эмодзи
        button_ru = Button(emoji="<:russia:1291223840994627595>", style=disnake.ButtonStyle.secondary, custom_id="select_ru")
        button_uk = Button(emoji="<:ukraine:1291223856752627723>", style=disnake.ButtonStyle.secondary, custom_id="select_uk")
        button_en = Button(emoji="<:kingdom_united:1291223870610866229>", style=disnake.ButtonStyle.secondary, custom_id="select_en")

        # Добавление кнопок в View
        self.add_item(button_ru)
        self.add_item(button_uk)
        self.add_item(button_en)

    async def send_initial_message(self, channel):
        """Отправляет первоначальное сообщение и сохраняет его идентификатор."""
        lang_translations = translations["ru"]  # По умолчанию русский
        embed = disnake.Embed(
            title=f"<:icons31:1274836415833833572> {lang_translations['title']}",
            description=lang_translations['description'],
        )

        gif_path = self.gif_mapping["ru"]  # Путь к гифке по умолчанию
        file = disnake.File(gif_path)  # Создаём объект File
        embed.set_image(url="attachment://working_24_7.gif")  # Укажите имя гифки по умолчанию

        # Отправка первоначального сообщения с выбором языка
        self.saved_message = await channel.send(embed=embed, view=self, file=file)
        self.saved_message_id = self.saved_message.id  # Сохранение идентификатора сообщения

    async def send_new_message(self, lang_code, channel):
        """Редактирует сохраненное сообщение с гифкой и переводом в зависимости от выбранного языка."""
        lang_translations = translations.get(lang_code, translations["ru"])  # По умолчанию русский
        embed = disnake.Embed(
            title=f"<:icons31:1274836415833833572> {lang_translations['title']}",
            description=lang_translations['description'],
        )

        gif_path = self.gif_mapping.get(lang_code, self.gif_mapping["ru"])  # По умолчанию русский

        # Проверка наличия файла
        if os.path.exists(gif_path):
            file = disnake.File(gif_path)  # Создаём объект File
            embed.set_image(url=f"attachment://{os.path.basename(gif_path)}")  # Устанавливаем гифку
            
            try:
                print(f"Пытаемся редактировать сообщение: {self.saved_message_id}")
                # Редактируем сохраненное сообщение с новым embed и гифкой
                await self.saved_message.edit(embed=embed, view=self, file=file)
                print("Сообщение успешно обновлено.")
            except disnake.Forbidden:
                print("У бота нет прав редактировать это сообщение.")
            except Exception as e:
                print(f"Произошла ошибка при редактировании сообщения: {e}")
        else:
            print(f"Файл не найден: {gif_path}")
            await channel.send("Гифка не найдена.")

        # Обновляем дату последнего сообщения
        update_last_sent(self.data, self.user_id)
        save_data(self.data)

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        """Проверка взаимодействия."""
        print(f"Получено взаимодействие: {interaction.type}, Пользователь: {interaction.user}")

        if interaction.type == disnake.InteractionType.component:
            if interaction.user == self.message.author:
                lang_code = None
                
                # Получаем custom_id из interaction.data
                custom_id = interaction.data.get('custom_id')
                if custom_id == "select_ru":
                    lang_code = "ru"
                elif custom_id == "select_uk":
                    lang_code = "uk"
                elif custom_id == "select_en":
                    lang_code = "en"
                
                if lang_code:
                    print(f"Выбранный язык: {lang_code}")

                    # Проверяем, был ли уже ответ
                    if not interaction.response.is_done():
                        await interaction.response.defer()  # Отложенный ответ
                        print("Ответ отложен, переходим к отправке нового сообщения...")
                        await self.send_new_message(lang_code, interaction.channel)  # Отправляем новое сообщение
                        return True
                    else:
                        print("Взаимодействие уже было обработано.")
    
        print("Взаимодействие не обработано: либо это не компонент, либо не автор сообщения.")
        return False  # Не выполняем действия, если пользователь не автор сообщения

async def send_auto_reply(message: disnake.Message, data, user_id):
    """Отправляет сообщение с гифкой в ответ на сообщение пользователя и обновляет дату последнего сообщения."""
    channel = message.channel
    if isinstance(channel, disnake.DMChannel) and not message.author.bot:
        view = LanguageSelector(message, data, user_id)
        await view.send_initial_message(channel)  # Отправляем первоначальное сообщение



