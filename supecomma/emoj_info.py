import disnake
from disnake.ext import commands
import json

class EmojiInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="app_emojis", description="Отправляет список всех эмодзи, доступных только для приложения.")
    @commands.cooldown(rate=1, per=10)
    async def app_emojis(self, inter: disnake.ApplicationCommandInteraction):
        # Получаем список всех эмодзи, доступных только приложению
        emojis = [emoji for emoji in inter.guild.emojis if emoji.available]

        # Создаем ембед с ограниченным количеством полей
        embed = disnake.Embed(
            title=f"Эмодзи приложения — {inter.guild.name}",
            description="Список эмодзи, которые доступны только для этого приложения.",
            color=disnake.Color.blue()
        )

        # Добавляем эмодзи в ембед, делая это в нескольких ембедах, если необходимо
        max_fields_per_embed = 25
        for i in range(0, len(emojis), max_fields_per_embed):
            embed = disnake.Embed(
                title=f"Эмодзи приложения — {inter.guild.name}",
                description="Список эмодзи, которые доступны только для этого приложения.",
                color=disnake.Color.blue()
            )
            for emoji in emojis[i:i + max_fields_per_embed]:
                embed.add_field(name=str(emoji), value=str(emoji), inline=True)
            await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(EmojiInfo(bot))

