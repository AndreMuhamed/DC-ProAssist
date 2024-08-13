import disnake
from disnake.ext import commands
from datetime import datetime, timedelta
from supecomma.config import ADMINS
import json

def setup_managemen(bot: commands.Bot):
    @bot.slash_command(name='adm_rewards', description='Установить монеты для пользователя.')
    async def adm_rewards(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.User, монеты: int):
        if not is_admin(inter.author):
            await inter.send("У вас нет прав для выполнения этой команды.", ephemeral=True)
            return

        user_id = str(пользователь.id)
        data = load_data()
        if user_id not in data:
            data[user_id] = {}

        # Установите монеты для пользователя
        data[user_id]['rewards'] = монеты
        save_data(data)
        await inter.send(f"Монеты для {пользователь.mention} установлены на {монеты}.", ephemeral=True)

    @bot.slash_command(name='adm_status', description='Установить статус для пользователя.')
    async def adm_status(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.User, статус: str):
        if not is_admin(inter.author):
            await inter.send("У вас нет прав для выполнения этой команды.", ephemeral=True)
            return

        user_id = str(пользователь.id)
        status_expiration = datetime.utcnow() + timedelta(days=90)
        data = load_data()
        if user_id not in data:
            data[user_id] = {}

        # Установите статус для пользователя
        data[user_id]['status'] = статус
        data[user_id]['status_expiration'] = status_expiration.isoformat()
        save_data(data)
        await inter.send(f"Статус для {пользователь.mention} установлен как '{статус}' и истечет {status_expiration.strftime('%Y-%m-%d %H:%M:%S')} UTC.", ephemeral=True)

    @bot.slash_command(name='adm_voice_online', description='Установить голосовой онлайн для пользователя.')
    async def adm_voice_online(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.User, секунд: int):
        if not is_admin(inter.author):
            await inter.send("У вас нет прав для выполнения этой команды.", ephemeral=True)
            return

        user_id = str(пользователь.id)
        data = load_data()
        if user_id not in data:
            data[user_id] = {}

        # Установите голосовой онлайн для пользователя
        formatted_time = format_seconds(секунд)
        data[user_id]['voice_online'] = formatted_time
        save_data(data)
        await inter.send(f"Голосовой онлайн для {пользователь.mention} установлен как '{formatted_time}'.", ephemeral=True)

    @bot.slash_command(name='adm_user_info', description='Получить информацию о пользователе по его ID.')
    async def adm_user_info(inter: disnake.ApplicationCommandInteraction, айди_пользователя: str):
        if not is_admin(inter.author):
            await inter.send("У вас нет прав для выполнения этой команды.", ephemeral=True)
            return

        data = load_data()
        user_info = data.get(айди_пользователя)
        user = await bot.fetch_user(int(айди_пользователя))

        if user_info:
            embed = disnake.Embed(title=f"Админ информация о {user.name}")
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(name="> ID пользователя:", value=f"<@{айди_пользователя}>", inline=False)
            embed.add_field(name="> Статус пользователя:", value=f"```{user_info.get('status', 'Не указан')}```", inline=False)
            embed.add_field(name="> Монеты у пользователя:", value=f"```{user_info.get('rewards', 0)}```", inline=False)
            embed.add_field(name="> Время в голосовом канале:", value=f"```{user_info.get('voice_online', 'Не указано')}```", inline=False)
            embed.add_field(name="> Последнее получение награды:", value=f"```{user_info.get('last_claim', 'Не указано')}```", inline=False)
            embed.add_field(name="> Профиль пользователя создан:", value=f"```{user_info.get('profile_created', 'Не указано')}```", inline=False)
            embed.add_field(name="> Время последнего контакта с ботом:", value=f"```{user_info.get('last_sent', 'Не указано')}```", inline=False)
            embed.add_field(name="> Ссылки на ВКонтакт:", value=f"```{user_info.get('vk', 'Не указан')}```", inline=False)
            embed.add_field(name="> Ссылки на Telegram:", value=f"```{user_info.get('telegram', 'Не указан')}```", inline=False)
            embed.add_field(name="> Ссылки на Instagram:", value=f"```{user_info.get('instagram', 'Не указан')}```", inline=False)
            
            
        else:
            embed = disnake.Embed(title="Ошибка", description=f"Пользователь с ID {айди_пользователя} не найден.")

        await inter.send(embed=embed, ephemeral=True)

    def format_seconds(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours} ч, {minutes} м"

    def is_admin(user):
        return str(user.id) in ADMINS

    def load_data():
        try:
            with open('admin/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(data):
        with open('admin/user_data.json', 'w') as f:
            json.dump(data, f, indent=4)

