import disnake
from disnake.ext import commands
from Translator.techno import get_user_language, translations  # Импортируем функцию и переводы

# Регистрация команды
def setup_test_command(bot: commands.Bot):
    @bot.slash_command(name='u_test', description=translations['en']["test_command_description"])  # Временное описание
    async def test(inter: disnake.ApplicationCommandInteraction):
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







