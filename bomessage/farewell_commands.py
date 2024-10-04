import disnake
from disnake.ext import commands
from Translator.farewell import translations


class FarewellCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        """Отправляет прощальное сообщение пользователю при его выходе с сервера."""
        try:
            # Отправляем прощальное сообщение на русском языке по умолчанию
            await self.send_farewell_message(member, 'ru')  # По умолчанию на русском

        except disnake.Forbidden:
            print(f"Не удалось отправить личное сообщение пользователю {member.name}. Проверьте настройки конфиденциальности.")
        except Exception as e:
            print(f"Произошла ошибка при отправке личного сообщения пользователю {member.name}: {str(e)}")

    async def send_farewell_message(self, member: disnake.Member, lang: str):
        """Отправляет прощальное сообщение с учетом выбранного языка."""
        locale = translations[lang]  # Получаем переводы для конкретного языка

        # Создаем сообщение embed
        embed = disnake.Embed(
            title=locale["farewell_title"],
            description=(locale["farewell_message"].format(member=member.mention) + "\n\n" +
                         locale["recommendation"] + "\n\n" +
                         locale["links"] + "\n" +
                         "• [Game Quest](https://www.youtube.com/@GameQuest_news)\n" +
                         "• [Nanson](https://www.youtube.com/@Nanson_CFM)\n" +
                         "• [ANIME INDUSTRY](https://www.youtube.com/@ANIME_INDUSTRY_UA)\n" +
                         "• [KINO INDUSTRY](https://www.youtube.com/@KINO_INDUSTRY_UA)\n" +
                         "• [Стримус](https://www.youtube.com/@Streamas)\n")
        )

        # Меняем местами изображения в embed
        embed.set_image(url="attachment://banner.jpg")  # Теперь это основное изображение
        embed.set_thumbnail(url="attachment://avatar.jpg")  # Теперь это миниатюра
        embed.set_footer(text=locale["footer_text"])  # Текст подвала

        # Добавляем кнопки для выбора языка (красные)
        view = await self.create_language_buttons(member, embed, lang)

        # Отправляем сообщение участнику с файлами
        files = [
            disnake.File("assets/banner.jpg", filename="banner.jpg"),
            disnake.File("assets/avatar.jpg", filename="avatar.jpg"),
        ]
        farewell_message = await member.send(embed=embed, view=view, files=files)

        # Сохраняем ID сообщения, чтобы редактировать его позже
        embed.view.message = farewell_message

        print(f"Прощальное сообщение отправлено пользователю {member.name}.")  # Для отладки

    async def create_language_buttons(self, member: disnake.Member, embed: disnake.Embed, lang: str):
        """Создает кнопки для выбора языка и кнопку поддержки с учетом выбранного языка."""
        locale = translations[lang]
        view = disnake.ui.View()

        # Добавляем кнопки для выбора языка (красные)
        languages = [
            ("Русский", "ru"),
            ("Українська", "uk"),
            ("English", "en"),
        ]
        for lang_name, lang_code in languages:
            button = disnake.ui.Button(label=lang_name, custom_id=lang_code, style=disnake.ButtonStyle.danger)
            button.callback = lambda interaction: self.button_callback(interaction, member, embed)
            view.add_item(button)

        # Добавляем кнопку поддержки с учетом перевода
        support_button_label = locale["support_button"]  # Получаем текст кнопки из translations
        support_button = disnake.ui.Button(label=support_button_label, style=disnake.ButtonStyle.danger, url="https://andremuhamed.nexcord.pro/multilink/creator/torex")
        view.add_item(support_button)

        return view

    async def button_callback(self, interaction: disnake.MessageInteraction, member: disnake.Member, embed: disnake.Embed):
        """Обрабатывает нажатия на кнопки выбора языка."""
        await interaction.response.defer()  # Подтверждаем взаимодействие
        lang_code = interaction.data['custom_id']  # Получаем custom_id из данных взаимодействия

        # Обновляем embed с новым языком
        locale = translations[lang_code]
        embed.title =locale["farewell_title"]
        embed.description = (
            locale["farewell_message"].format(member=member.mention) + "\n\n" +
            locale["recommendation"] + "\n\n" +
            locale["links"] + "\n" +
            "• [Game Quest](https://www.youtube.com/@GameQuest_news)\n" +
            "• [Nanson](https://www.youtube.com/@Nanson_CFM)\n" +
            "• [ANIME INDUSTRY](https://www.youtube.com/@ANIME_INDUSTRY_UA)\n" +
            "• [KINO INDUSTRY](https://www.youtube.com/@KINO_INDUSTRY_UA)\n" +
            "• [Стримус](https://www.youtube.com/@Streamas)\n"
        )
        embed.set_footer(text=locale["footer_text"])  # Текст подвала

        # Создаем новые кнопки с обновленным языком
        view = await self.create_language_buttons(member, embed, lang_code)

        # Редактируем сообщение с прощанием и обновленными кнопками
        await interaction.message.edit(embed=embed, view=view)

def setup(bot):
    bot.add_cog(FarewellCommand(bot))




