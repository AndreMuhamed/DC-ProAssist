import disnake
from disnake.ext import commands
from Translator.handling import translations  # Импортируем переводы


class ErrorHandlingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            try:
                user_language = 'ru'  # По умолчанию русский

                # Получаем переводы для конкретного языка
                locale = translations[user_language]

                # Создаем сообщение embed
                command_used = ctx.message.content
                embed = disnake.Embed(
                    title=f"<:icons42:1274836509249245327> {locale['error_title']}",
                    description=locale["error_message"].format(command=command_used),
                )

                # Устанавливаем аватарку для embed
                bot_avatar_url = "https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png?"
                embed.set_thumbnail(url=bot_avatar_url)

                # Добавляем поле с подсказкой
                embed.add_field(name=locale['clue'], value=locale['hint'], inline=False)

                # Создаем представление с кнопками
                view = await self.create_language_buttons(command_used)

                # Отправляем сообщение об ошибке
                error_message = await ctx.author.send(embed=embed, view=view)

                # Сохраняем ID сообщения для редактирования
                view.message_id = error_message.id

            except disnake.Forbidden:
                print(f"Не удалось отправить личное сообщение пользователю {ctx.author.name}. Проверьте настройки конфиденциальности.")
            except Exception as e:
                print(f"Произошла ошибка: {str(e)}")

    async def create_language_buttons(self, original_command: str):
        """Создает кнопки для выбора языка с эмодзи."""
        view = disnake.ui.View()

        # Создаем кнопки и добавляем их в представление
        button_ru = disnake.ui.Button(emoji="<:russia:1291223840994627595>", style=disnake.ButtonStyle.secondary, custom_id="select_ru")
        button_uk = disnake.ui.Button(emoji="<:ukraine:1291223856752627723>", style=disnake.ButtonStyle.secondary, custom_id="select_uk")
        button_en = disnake.ui.Button(emoji="<:kingdom_united:1291223870610866229>", style=disnake.ButtonStyle.secondary, custom_id="select_en")

        # Привязываем обработчики к кнопкам
        button_ru.callback = lambda interaction: self.set_language(interaction, "ru", original_command)
        button_uk.callback = lambda interaction: self.set_language(interaction, "uk", original_command)
        button_en.callback = lambda interaction: self.set_language(interaction, "en", original_command)

        # Добавляем кнопки в представление
        view.add_item(button_ru)
        view.add_item(button_uk)
        view.add_item(button_en)

        return view

    async def set_language(self, interaction: disnake.MessageInteraction, lang_code: str, original_command: str):
        """Обновляет язык в сообщении и настраивает embed."""
        await interaction.response.defer()  # Подтверждаем взаимодействие

        # Обновляем embed с новым языком
        locale = translations[lang_code]
        embed = disnake.Embed(
            title=f"<:icons42:1274836509249245327> {locale['error_title']}",
            description=locale["error_message"].format(command=original_command),
        )

        # Устанавливаем аватарку для embed
        bot_avatar_url = "https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png?"
        embed.set_thumbnail(url=bot_avatar_url)

        # Обновляем поле с подсказкой
        embed.add_field(name=locale['clue'], value=locale['hint'], inline=False)

        # Создаем новые кнопки с обновленным языком
        new_view = await self.create_language_buttons(original_command)

        # Редактируем сообщение с ошибкой и обновленными кнопками
        await interaction.message.edit(embed=embed, view=new_view)


def setup(bot):
    bot.add_cog(ErrorHandlingCog(bot))











