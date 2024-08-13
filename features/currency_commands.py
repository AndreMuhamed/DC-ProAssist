import disnake
from disnake.ext import commands
import json

def setup_currency_commands(bot: commands.Bot):
    @bot.slash_command(name='transfer', description='Передать валюту другому пользователю.')
    async def transfer_currency(inter: disnake.ApplicationCommandInteraction, получатель: disnake.Member, количество: int):
        try:
            отправитель_id = str(inter.author.id)
            получатель_id = str(получатель.id)
            
            data = load_data()
            
            # Убедитесь, что оба пользователя существуют в данных
            if отправитель_id not in data:
                await inter.send("У вас нет валюты для передачи.", ephemeral=True)
                return
            if получатель_id not in data:
                data[получатель_id] = {"rewards": 0, "transactions": []}

            отправитель_валюта = data[отправитель_id].get('rewards', 0)
            
            # Проверка, что у отправителя достаточно валюты
            if отправитель_валюта < количество:
                await inter.send("У вас недостаточно валюты для передачи.", ephemeral=True)
                return
            
            # Расчет комиссии
            комиссия = int(количество * 0.025)
            общая_сумма = количество + комиссия

            if отправитель_валюта < общая_сумма:
                await inter.send(f"У вас недостаточно валюты для передачи с учетом комиссии {комиссия} монет.", ephemeral=True)
                return

            # Обновление данных о валюте
            data[отправитель_id]['rewards'] -= общая_сумма
            data[получатель_id]['rewards'] += количество
            
            # Запись транзакции
            data[отправитель_id].setdefault('transactions', []).append(
                f"Вы передали {количество} монет пользователю {получатель.mention} с комиссией {комиссия} монет."
            )
            data[получатель_id].setdefault('transactions', []).append(
                f"Вы получили {количество} монет от пользователя {inter.author.mention}."
            )
            
            save_data(data)
            
            # Получение серверного аватара
            серверный_аватар = inter.author.guild_avatar.url if inter.author.guild_avatar else inter.author.display_avatar.url

            embed = disnake.Embed(
                title="<:Stickerus7:1269746114932900041> Перевод валюты!",
                description=f"Пользователь {inter.author.mention} щедро передал **{количество}** монет {получатель.mention} с комиссией **{комиссия}** монет.",
            )
            embed.set_thumbnail(url=серверный_аватар)
            embed.set_footer(text="Спасибо за использование нашей системы валют!")

            await inter.send(embed=embed)
        
        except Exception:
            await inter.send("Произошла ошибка при выполнении команды. Пожалуйста, попробуйте позже.", ephemeral=True)

def load_data():
    try:
        with open('admin/user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_data(data):
    try:
        with open('admin/user_data.json', 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        print("Ошибка записи данных.")

# Добавление команд в бот
def setup(bot):
    setup_currency_commands(bot)


