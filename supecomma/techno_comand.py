import disnake
from disnake.ext import commands
from Translator.techno import get_user_language, translations
from admin.error_log import handle_exception  # Імпортуємо функцію для обробки помилок

def setup_test_command(bot: commands.Bot):
    @bot.slash_command(name='u_test', description=translations['en']["test_command_description"])
    async def test(inter: disnake.ApplicationCommandInteraction):
        try:
            # Определяем язык пользователя
            user_language = get_user_language(inter)
            locale = translations[user_language]

            # Получаем перевод на нужном языке
            title = locale["bot_confused_title"]
            description = locale["bot_confused_description"]

            # Создание сообщения с embed
            embed = disnake.Embed(
                title=title,
                description=description,
            )

            # Установка изображения (gif)
            with open('assets/Error.gif', 'rb') as f:
                file = disnake.File(f, filename='Confused.gif')
                embed.set_image(url='attachment://Confused.gif')

            # Отправка сообщения
            await inter.send(embed=embed, file=file)

        except Exception as e:
            handle_exception(e)  # Обрабатываем исключение








