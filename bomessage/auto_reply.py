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

        # Создание кнопок с эмодзи
        button_ru = Button(emoji="<:russia:1291223840994627595>", style=disnake.ButtonStyle.secondary, custom_id="select_ru")
        button_uk = Button(emoji="<:ukraine:1291223856752627723>", style=disnake.ButtonStyle.secondary, custom_id="select_uk")
        button_en = Button(emoji="<:kingdom_united:1291223870610866229>", style=disnake.ButtonStyle.secondary, custom_id="select_en")

        # Добавление кнопок в View
        self.add_item(button_ru)
        self.add_item(button_uk)
        self.add_item(button_en)

    async def send_new_message(self, lang_code, interaction):
        """Редактирует текущее сообщение с гифкой и переводом в зависимости от выбранного языка."""
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
                # Редактируем текущее сообщение с embed и гифкой
                await interaction.response.edit_message(embed=embed, file=file)
            except disnake.Forbidden:
                print("У бота нет прав редактировать это сообщение.")
            except Exception as e:
                print(f"Произошла ошибка при редактировании сообщения: {e}")
        else:
            print(f"File not found: {gif_path}")
            await interaction.response.edit_message(content="Гифка не найдена.")

        # Обновляем дату последнего сообщения
        update_last_sent(self.data, self.user_id)
        save_data(self.data)

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        """Проверка взаимодействия."""
        # Добавляем отладочный вывод
        print(f"Interaction received: {interaction.type}, User: {interaction.user}")
        
        if interaction.type == disnake.InteractionType.component:
            if interaction.user == self.message.author:
                lang_code = None
                # Получаем custom_id из interaction.data
                if interaction.data.get('custom_id') == "select_ru":
                    lang_code = "ru"
                elif interaction.data.get('custom_id') == "select_uk":
                    lang_code = "uk"
                elif interaction.data.get('custom_id') == "select_en":
                    lang_code = "en"
                
                if lang_code:
                    print(f"Selected language: {lang_code}")  # Отладочный вывод
                    await self.send_new_message(lang_code, interaction)  # Редактируем текущее сообщение
                    return True
        
        print("Interaction not processed: either not a component or not the message author.")
        return False  # Не выполняем действия, если пользователь не автор сообщения

async def send_auto_reply(message: disnake.Message, data, user_id):
    """Отправляет сообщение с гифкой в ответ на сообщение пользователя и обновляет дату последнего сообщения."""
    channel = message.channel
    if isinstance(channel, disnake.DMChannel) and not message.author.bot:
        embed = disnake.Embed(
            title=f"<:icons31:1274836415833833572> {translations['ru']['title']}",
            description=translations['ru']['description'],
        )
        
        # Устанавливаем гифку по умолчанию
        gif_path = "assets/working_24_7.gif"
        if os.path.exists(gif_path):
            file = disnake.File(gif_path)  # Создаём объект File
            
            # Отправка первоначального сообщения с выбором языка
            embed.set_image(url="attachment://working_24_7.gif")  # Укажите имя гифки по умолчанию
            view = LanguageSelector(message, data, user_id)
            await channel.send(embed=embed, view=view, file=file)
        else:
            await channel.send("Гифка по умолчанию не найдена.")
























