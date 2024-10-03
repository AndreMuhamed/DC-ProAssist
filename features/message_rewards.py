import disnake   
from disnake.ext import commands
import json
import os
from Translator.message import translations  # Импортируем переводы

class MessageRewards(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        data = self.load_data()

        # Проверяем, если пользователь еще не получил награду за первое сообщение
        if user_id not in data or "rewarded" not in data[user_id]:
            # Обновляем данные пользователя
            if user_id not in data:
                data[user_id] = {"rewards": 0}
            else:
                # Убедитесь, что rewards является целым числом
                if isinstance(data[user_id]["rewards"], str):
                    data[user_id]["rewards"] = int(data[user_id]["rewards"])

            data[user_id]["rewards"] += 1450
            data[user_id]["rewarded"] = True
            self.save_data(data)

            # Отправляем сообщение с наградой на русском языке
            try:
                locale = translations["ru"]  # Получаем переводы на русском
                embed = disnake.Embed(
                    title=f"<:icons55:1274836863483383869> {locale['reward_title']}",
                    description=locale["reward_description"],
                ).add_field(
                    name=locale["reward_field"], 
                    value=locale["reward_field_value"].format(1450), 
                    inline=False
                ).set_footer(
                    text=locale["reward_footer"]
                ).set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png"
                )

                # Создаем кнопки для выбора языка
                view = await self.create_language_buttons(embed, message.author)
                await message.author.send(embed=embed, view=view)
            except disnake.Forbidden:
                print(f"Не удалось отправить личное сообщение пользователю {message.author.id}")

        await self.bot.process_commands(message)

    async def create_language_buttons(self, embed: disnake.Embed, user: disnake.User):
        """Создает кнопки для выбора языка с эмодзи."""
        view = disnake.ui.View()

        # Создаем кнопки и добавляем их в представление
        button_ru = disnake.ui.Button(emoji="<:russia:1291223840994627595>", style=disnake.ButtonStyle.secondary, custom_id="select_ru")
        button_uk = disnake.ui.Button(emoji="<:ukraine:1291223856752627723>", style=disnake.ButtonStyle.secondary, custom_id="select_uk")
        button_en = disnake.ui.Button(emoji="<:kingdom_united:1291223870610866229>", style=disnake.ButtonStyle.secondary, custom_id="select_en")

        # Привязываем обработчики к кнопкам
        button_ru.callback = lambda interaction: self.set_language(interaction, "ru", embed)
        button_uk.callback = lambda interaction: self.set_language(interaction, "uk", embed)
        button_en.callback = lambda interaction: self.set_language(interaction, "en", embed)

        # Добавляем кнопки в представление
        view.add_item(button_ru)
        view.add_item(button_uk)
        view.add_item(button_en)

        return view

    async def set_language(self, interaction: disnake.MessageInteraction, lang_code: str, embed: disnake.Embed):
        """Обрабатывает выбор языка и обновляет сообщение с наградой."""
        await interaction.response.defer()  # Подтверждаем взаимодействие

        # Получаем перевод на выбранном языке
        locale = translations[lang_code]

        # Обновляем embed с наградой на выбранном языке
        embed.title = f"<:icons55:1274836863483383869> {locale['reward_title']}"
        embed.description = locale["reward_description"]  # Здесь не нужно форматировать
        embed.set_footer(text=locale["reward_footer"])

        # Обновляем поле с наградой с форматированием
        embed.clear_fields()
        embed.add_field(name=locale["reward_field"], value=locale["reward_field_value"].format(1450), inline=False)

        # Редактируем сообщение с наградой
        await interaction.message.edit(embed=embed)

    def load_data(self):
        user_data_path = 'admin/user_data.json'
        if not os.path.exists(user_data_path):
            print(f"Файл {user_data_path} не найден, создается новый.")
            self.save_data({})
            return {}

        try:
            with open(user_data_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
            return {}

    def save_data(self, data):
        try:
            with open('admin/user_data.json', 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Ошибка записи данных пользователя: {e}")

def setup(bot: commands.Bot):
    bot.add_cog(MessageRewards(bot))
