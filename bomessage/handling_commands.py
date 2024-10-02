import disnake
from disnake.ext import commands
from Translator.handling import translations, get_user_language  # Импортируем переводы

class ErrorHandlingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            # Определение языка пользователя
            user_language = get_user_language(ctx)  # Измените на ctx, если это не interaction
            
            # Получаем переводы для соответствующего языка
            lang_translations = translations.get(user_language, translations['ru'])  # По умолчанию русский

            # Подставляем команду в описание
            description = lang_translations['description'].format(command=ctx.message.content)

            embed = disnake.Embed(
                title=lang_translations['title'],
                description=description,
            )
            embed.add_field(name="Подсказка:", value=lang_translations['hint'])
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png')
            await ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(ErrorHandlingCog(bot))

