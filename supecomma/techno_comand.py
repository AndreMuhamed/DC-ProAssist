import disnake
from disnake.ext import commands

def setup_test_command(bot: commands.Bot):
    @bot.slash_command(name='u_test', description='Не жми сюда, если не хочешь увидеть смерть!')
    async def test(inter: disnake.ApplicationCommandInteraction):
        # Создание сообщения с embed
        embed = disnake.Embed(
            title="<:Stickerus11:1269746147707060387> Бот запутался!",
            description="Ой, кажется **что-то** пошло не так. Мы уже пытаемся разобраться в проблеме! **Но это не точно**",
        )

        # Установка изображения (gif)
        with open('assets/Error.gif', 'rb') as f:
            file = disnake.File(f, filename='Confused.gif')
            embed.set_image(url='attachment://Confused.gif')

        # Отправка сообщения
        await inter.send(embed=embed, file=file)



