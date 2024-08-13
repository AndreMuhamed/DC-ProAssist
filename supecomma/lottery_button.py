import disnake
from disnake.ext import commands
from disnake.ui import Button, View
from supecomma.config import ALLOWED_ROLES
import random
import json
import asyncio
from datetime import datetime, timedelta

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.participants = set()  # Хранение участников

    def load_data(self):
        try:
            with open('admin/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def save_data(self, data):
        try:
            with open('admin/user_data.json', 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"File IO Error: {e}")

    def ensure_user_profile(self, data, user_id):
        if user_id not in data:
            data[user_id] = {"rewards": 0}
            self.save_data(data)

    @commands.slash_command(name='adm_lottery', description='Запустить лотерею от Online Shop.')
    async def start_lottery(self, ctx, время: int, выигрыш: int, канал: disnake.TextChannel):
        """Запускает лотерею на указанное время (в секундах) с кнопкой для участия и выбором канала."""
        try:
            # Проверка ролей пользователя
            user_roles = {str(role.id) for role in ctx.author.roles}
            if not any(role in ALLOWED_ROLES for role in user_roles):
                await ctx.send(
                    embed=disnake.Embed(
                        title="<:Stickerus15:1269746177356861531> Ошибка от Online Shop!",
                        description="У вас нет необходимой роли для запуска этой команды.",
                    ).set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png'),
                    ephemeral=True
                )
                return

            if время <= 0:
                await ctx.send(
                    embed=disnake.Embed(
                        title=" <:Stickerus15:1269746177356861531> Ошибка от Online Shop!",
                        description="Продолжительность лотереи должна быть положительным числом.",
                    ).set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png'),
                    ephemeral=True
                )
                return

            self.participants.clear()  # Очистка списка участников

            # Создание кнопки для участия в лотерее
            button = Button(label="Участвовать", style=disnake.ButtonStyle.primary, custom_id="lottery_join")
            view = View()
            view.add_item(button)

            # Определение времени завершения лотереи
            end_time = datetime.utcnow() + timedelta(seconds=время)

            # Создание эмбеда для сообщения с обратным отсчетом времени
            countdown_embed = disnake.Embed(
                title="<:Stickerus6:1269746107202797588> Лотерея от Online Shop!",
                description=f"Нажмите на кнопку ниже, чтобы участвовать.\n\n"
                            f"**Оставшееся время:** {время} секунд\n"
                            f"**Награда:** {выигрыш} монет",
            ).set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png')

            countdown_message = await канал.send(
                embed=countdown_embed,
                view=view
            )

            # Отправка сообщения инициатору
            await ctx.send(
                embed=disnake.Embed(
                    title="<:Stickerus6:1269746107202797588> Лотерея запущена от Online Shop!",
                    description=f"Вы запустили лотерею! Ожидайте, пока она завершится.",
                ).set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png'),
                ephemeral=True
            )

            # Обновление эмбеда с обратным отсчетом времени
            while datetime.utcnow() < end_time:
                remaining_time = int((end_time - datetime.utcnow()).total_seconds())
                countdown_embed.description = (
                    f"Нажмите на кнопку ниже, чтобы участвовать.\n\n"
                    f"**Оставшееся время:** {remaining_time} секунд\n"
                    f"**Награда:** {выигрыш} монет"
                )
                await countdown_message.edit(embed=countdown_embed)
                await asyncio.sleep(1)  # Обновляем каждый 1 секунду

            # Определение победителя
            if not self.participants:
                no_participants_embed = disnake.Embed(
                    title="<:Stickerus6:1269746107202797588> Лотерея завершена от Online Shop!",
                    description="К сожалению, участники не найдены. Возможно, никто не присоединился к лотерее.",
                ).set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png')
                await канал.send(embed=no_participants_embed)
                return

            winner_id = random.choice(list(self.participants))
            winner = self.bot.get_user(int(winner_id))

            # Загрузка данных пользователей
            data = self.load_data()
            self.ensure_user_profile(data, str(winner_id))

            # Начисление монет победителю
            data[str(winner_id)]['rewards'] += выигрыш
            self.save_data(data)

            # Создание эмбеда с результатами
            results_embed = disnake.Embed(
                title="<:Stickerus6:1269746107202797588> Лотерея завершена от Online Shop!",
                description=f"Поздравляем {winner.mention}! Вы выиграли лотерею и получили {выигрыш} монет!\n\n"
                            f"Участники лотереи: {', '.join(f'<@{p}>' for p in self.participants)}",
            ).set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png')

            # Отправка результатов
            await канал.send(embed=results_embed)
        except Exception as e:
            await ctx.send(
                embed=disnake.Embed(
                    title="<:Stickerus15:1269746177356861531> Ошибка от Online Shop!",
                    description=f"Произошла ошибка: {e}",
                ).set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png'),
                ephemeral=True
            )

    @commands.Cog.listener()
    async def on_interaction(self, inter: disnake.Interaction):
        try:
            if inter.type == disnake.InteractionType.component and inter.data.get('custom_id') == "lottery_join":
                user_id = str(inter.user.id)
                if user_id not in self.participants:
                    self.participants.add(user_id)  # Добавление пользователя в список участников

                    # Создание эмбеда для подтверждения участия
                    joined_embed = disnake.Embed(
                        title="<:Stickerus21:1269746227872796713> Участие подтверждено от Online Shop!",
                        description=f"{inter.user.mention}, Вы успешно присоединились к лотерее. Пожалуйста, не нажимайте на кнопку повторно.",
                    ).set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png')
                    await inter.response.send_message(embed=joined_embed, ephemeral=True)
                else:
                    await inter.response.send_message(
                        embed=disnake.Embed(
                            title="<:Stickerus21:1269746227872796713> Уже участвуете в лотерее от Online Shop!",
                            description="Вы уже участвуете в лотерее. Пожалуйста, не нажимайте на кнопку повторно.",
                        ).set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png'),
                        ephemeral=True
                    )
            else:
                print(f"Unknown interaction type: {inter.type}")
        except Exception as e:
            print(f"Error handling interaction: {e}")

def setup(bot):
    bot.add_cog(Lottery(bot))









