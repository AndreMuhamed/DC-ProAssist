import disnake
from disnake.ext import commands

class WelcomeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='welcome')
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx, member: disnake.Member):
        """Отправляет приветственное сообщение пользователю при его присоединении."""
        embed = disnake.Embed(
            title="<:Stickerus7:1269746114932900041> Добро пожаловать на сервер!",
            description=(
                f"Привет, {member.mention}! Ты находишься на одном из проектов **Андрея Мухамеда**.\n\n"
                "Рекомендуем подписаться на его другие проекты на YouTube, нажав на кнопки ниже под этим сообщением. **Заранее благодарим!**"
            ),
        )
        # Добавьте кнопки с ссылками на проекты
        view = disnake.ui.View()
        projects = [
            ("Game Quest", "https://www.youtube.com/@GameQuest_news"),
            ("Nanson", "https://www.youtube.com/@Nanson_CFM"),
            ("ANIME INDUSTRY", "https://www.youtube.com/@ANIME_INDUSTRY_UA"),
            ("KINO INDUSTRY", "https://www.youtube.com/@KINO_INDUSTRY_UA"),
            ("Стримус", "https://www.youtube.com/@Streamas"),
        ]
        for name, url in projects:
            view.add_item(disnake.ui.Button(label=name, url=url, style=disnake.ButtonStyle.link))
        
        try:
            files = [
                disnake.File("assets/avatar.jpg", filename="avatar.jpg"),
                disnake.File("assets/banner.jpg", filename="banner.jpg"),
            ]
            embed.set_thumbnail(url="attachment://avatar.jpg")
            embed.set_image(url="attachment://banner.jpg")
            embed.set_footer(text="Спасибо за вашу будущую активность!")
            await member.send(embed=embed, view=view, files=files)
            await ctx.send(f"Приветственное сообщение отправлено пользователю {member.mention}.")
        except disnake.Forbidden:
            await ctx.send(f"Не удалось отправить личное сообщение пользователю {member.mention}. Проверьте настройки конфиденциальности.")
        except Exception as e:
            await ctx.send(f"Произошла ошибка при отправке личного сообщения пользователю {member.mention}: {str(e)}")

def setup(bot):
    bot.add_cog(WelcomeCommand(bot))
