import disnake
from disnake.ext import commands

class MentionResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message):
            latency = round(self.bot.latency * 1000)  # Пинг в миллисекундах
            embed = disnake.Embed(
                title=f"<:Stickerus15:1269746177356861531> Меня упомянул — {message.author.name}!",
                description=(
                    "Привет! Я здесь и всегда готов **помочь** и внести вклад в проекты **Андрея Мухамеда**.\n\n"
                    f"Мой прекрасный пинг: {latency} мс.\n"
                    "Мои создатели: <@768782555171782667> и <@787093771115692062>\n"
                    "Website Muhameda: [andremuhamed.nexcord.pro](https://andremuhamed.nexcord.pro)"
                ),
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)  # Установка аватарки бота
            embed.set_footer(text="Благодарим за использование наших сервисов!")
            await message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(MentionResponse(bot))


