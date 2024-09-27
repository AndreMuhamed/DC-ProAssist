import disnake
from disnake.ext import commands
from Translator.techno import get_user_language, translations  # Импортируем функцию и переводы

def setup_test_command(bot: commands.Bot):
    @bot.slash_command(name='u_test', description='Не жми сюда, если не хочешь увидеть смерть!')
    async def test(inter: disnake.ApplicationCommandInteraction):
        # Определяем язык пользователя
        user_language = get_user_language(inter)

        # Получаем перевод на нужном языке
        title = translations[user_language]["bot_confused_title"]
        description = translations[user_language]["bot_confused_description"]

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






