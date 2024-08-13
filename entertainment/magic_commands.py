import disnake
from disnake.ext import commands
import random

def setup_magic_commands(bot: commands.Bot):
    @bot.slash_command(name='magic_tetris', description='Задайте любой вопрос магическому тетрису.')
    async def magic_tetris(inter: disnake.ApplicationCommandInteraction, вопрос: str):
        responses = [
            "Бесспорно",
            "Предрешено",
            "Никаких сомнений",
            "Определённо да",
            "Можешь быть уверен в этом",
            "Мне кажется - да",
            "Вероятнее всего",
            "Хорошие перспективы",
            "Знаки говорят - да",
            "Да",
            "Пока не ясно, попробуй снова",
            "Спроси позже",
            "Лучше не рассказывать",
            "Сейчас нельзя предсказать",
            "Сконцентрируйся и спроси опять",
            "Даже не думай",
            "Мой ответ - нет",
            "По моим данным - нет",
            "Перспективы не очень хорошие",
            "Весьма сомнительно"
        ]

        response = random.choice(responses)
        embed = disnake.Embed(
            title="<:Stickerus21:1269746227872796713> Магический тетрис!",
            description=f"**Вопрос:** {вопрос}\n**Ответ:** {response}",
        )
        embed.set_thumbnail(url="https://i.gifer.com/3Oo9g.gif")

        await inter.send(embed=embed)

