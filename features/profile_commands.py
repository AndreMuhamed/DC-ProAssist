import disnake
from disnake.ext import commands
from admin.data_handler import load_data, save_data, ensure_user_profile
from admin.error_log import handle_exception
import re
import os
import json
from datetime import datetime

def setup_profile_commands(bot: commands.Bot):
    @bot.slash_command(name='profile', description='Просмотреть профиль пользователя.')
    async def profile(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.User = None):
        await inter.response.defer()  # Уведомляем, что команда обрабатывается

        try:
            user = пользователь or inter.author
            user_id = str(user.id)
            data = load_data()  # Загрузка актуальных данных
            ensure_user_profile(data, user_id)  # Проверка и создание профиля

            user_data = data.get(user_id, {})
            avatar_url = user.display_avatar.url if user.display_avatar else user.default_avatar.url
            status = user_data.get('status', 'Нет статуса')
            rewards = user_data.get('rewards', 0)
            voice_online = user_data.get('voice_online', '0 ч, 0 м')
            vk = user_data.get('vk', 'Не указано')
            telegram = user_data.get('telegram', 'Не указано')
            instagram = user_data.get('instagram', 'Не указано')
            profile_created = user_data.get('profile_created', 'Не указано')

            embed = disnake.Embed(
                title=f"Профиль — {user.name}",
                description=f"> **Статус:**\n```{status}```",
            )
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="> **Монеты:**", value=f"```{rewards}```", inline=True)
            embed.add_field(name="> **Голосовой онлайн:**", value=f"```{voice_online}```", inline=True)
            embed.add_field(name="> **Создан профиль:**", value=f"```{profile_created}```", inline=True)

            buttons = []

            if vk != 'Не указано':
                buttons.append(disnake.ui.Button(label="VKontakte", url=vk))
            if telegram != 'Не указано':
                buttons.append(disnake.ui.Button(label="Telegram", url=telegram))
            if instagram != 'Не указано':
                buttons.append(disnake.ui.Button(label="Instagram", url=instagram))

            # Добавление кнопки "Купить монеты"
            buy_coins_button = disnake.ui.Button(
                label="Купить монеты",
                style=disnake.ButtonStyle.danger,
                custom_id="buy_coins"
            )

            components = [disnake.ui.ActionRow(*buttons, buy_coins_button)] if buttons else [disnake.ui.ActionRow(buy_coins_button)]

            # Отправка ответа
            await inter.edit_original_response(embed=embed, components=components)
        
        except Exception as e:
            handle_exception(e)  # Логируем ошибку, но не отправляем сообщение пользователю

    @bot.listen("on_button_click")
    async def on_button_click(interaction: disnake.MessageInteraction):
        try:
            if interaction.component.custom_id == "buy_coins":
                seller_avatar_url = "https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png"  # Замените на URL аватара продавца
                
                # Создание эмбеда для отправки сообщения
                embed = disnake.Embed(
                    title="<:Stickerus8:1269746123673960663> Покупка монет в Online Shop!",
                    description="Спасибо за интерес к покупке монет! Для завершения покупки, пожалуйста, свяжитесь с продавцом.",
                )
                embed.add_field(
                    name="Ссылка на продавцов:",
                    value="<@768782555171782667> или <@787093771115692062>"  # ID продавца, на которого можно ссылаться
                )
                embed.set_thumbnail(url=seller_avatar_url)
                
                await interaction.send(embed=embed, ephemeral=True)
    
        except Exception as e:
            handle_exception(e)  # Логируем ошибку, но не отправляем сообщение пользователю

    @bot.slash_command(name='profile_socials', description='Добавить ссылки на социальные сети.')
    async def profile_socials(inter: disnake.ApplicationCommandInteraction, vkontakte: str = "", telegram: str = "", instagram: str = ""):
        await inter.response.defer()  # Уведомляем, что команда обрабатывается

        try:
            user_id = str(inter.author.id)
            data = load_data()  # Загрузка актуальных данных
            ensure_user_profile(data, user_id)  # Проверка и создание профиля

            if vkontakte and not validate_vk_url(vkontakte):
                await inter.edit_original_response(content="Некорректный URL для VKontakte.", ephemeral=True)
                return
            if telegram and not validate_telegram_url(telegram):
                await inter.edit_original_response(content="Некорректный URL для Telegram.", ephemeral=True)
                return
            if instagram and not validate_instagram_url(instagram):
                await inter.edit_original_response(content="Некорректный URL для Instagram.", ephemeral=True)
                return

            update_user_data(data, user_id, vkontakte, telegram, instagram)
            save_data(data)  # Сохранение данных после обновления
            await inter.edit_original_response(content="Ваши социальные сети обновлены!", ephemeral=True)
        
        except Exception as e:
            handle_exception(e)  # Логируем ошибку, но не отправляем сообщение пользователю

def validate_vk_url(url):
    """Проверяет корректность URL для VKontakte."""
    return re.match(r'^https://vk\.com/\w+$', url)

def validate_telegram_url(url):
    """Проверяет корректность URL для Telegram."""
    return re.match(r'^https://t\.me/\w+$', url)

def validate_instagram_url(url):
    """Проверяет корректность URL для Instagram."""
    return re.match(r'^https://www\.instagram\.com/\w+$', url)

def update_user_data(data, user_id, vkontakte, telegram, instagram):
    if user_id in data:
        user_data = data[user_id]
        if vkontakte:
            user_data["vk"] = vkontakte
        if telegram:
            user_data["telegram"] = telegram
        if instagram:
            user_data["instagram"] = instagram
    else:
        data[user_id] = {
            "status": "Нет статуса",
            "rewards": 0,
            "voice_online": "0 ч, 0 м",
            "vk": vkontakte or "Не указано",
            "telegram": telegram or "Не указано",
            "instagram": instagram or "Не указано",
            "profile_created": datetime.utcnow().strftime("%d.%m.%Y")
        }

def load_data():
    user_data_path = 'admin/user_data.json'
    if os.path.exists(user_data_path):
        try:
            with open(user_data_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    else:
        return {}

def save_data(data):
    user_data_path = 'admin/user_data.json'
    try:
        with open(user_data_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Ошибка записи данных пользователя: {e}")



