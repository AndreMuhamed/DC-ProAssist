import disnake
from disnake.ext import commands

class FarewellCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        """Отправляет сообщение, когда участник покидает сервер."""
        embed = disnake.Embed(
            title="<:Stickerus18:1269746200270340236> Участник покинул сервер!",
            description=(
                f"К сожалению, {member.mention}, ты покинул наш сервер. Надеемся, что тебе понравилось здесь и ты вернёшься в будущем.\n\n"
                "Ты всегда можешь подписаться на проекты **Андрея Мухамеда** на YouTube, нажав на кнопки ниже. **Будем рады видеть тебя снова!**"
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
            print(f"Прощальное сообщение отправлено пользователю {member.mention}.")
        except disnake.Forbidden:
            print(f"Не удалось отправить личное сообщение пользователю {member.mention}. Проверьте настройки конфиденциальности.")
        except Exception as e:
            print(f"Произошла ошибка при отправке личного сообщения пользователю {member.mention}: {str(e)}")

def setup(bot):
    bot.add_cog(FarewellCommand(bot))

