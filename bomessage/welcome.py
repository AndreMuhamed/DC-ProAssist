import disnake
from disnake.ext import commands
from Translator.welco import get_user_language, translations  # Импортируем функцию и переводы

class WelcomeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        """Отправляет приветственное сообщение пользователю при его присоединении."""
        # Получаем язык пользователя через preferred_locale
        user_language = member.locale if hasattr(member, 'locale') else 'en'  # Если атрибута нет, используем английский по умолчанию
        locale = translations.get(user_language, translations['en'])  # Используем переводы для конкретного языка или английский по умолчанию

        embed = disnake.Embed(
            title="<:Stickerus7:1269746114932900041> " + locale["welcome_title"],  # Перевод заголовка
            description=(
                f"{locale['welcome_message'].format(member=member.mention)}\n\n" +  # Перевод приветственного сообщения
                locale["recommendation"]
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
            embed.set_footer(text=locale["footer_text"])  # Перевод текста в подвале
            
            await member.send(embed=embed, view=view, files=files)  # Отправляем сообщение новому участнику
            print(f"Приветственное сообщение отправлено пользователю {member.name}.")  # Для отладки
        
        except disnake.Forbidden:
            print(f"Не удалось отправить личное сообщение пользователю {member.name}. Проверьте настройки конфиденциальности.")
        except Exception as e:
            print(f"Произошла ошибка при отправке личного сообщения пользователю {member.name}: {str(e)}")  # Печатаем текст ошибки

def setup(bot):
    bot.add_cog(WelcomeCommand(bot))



