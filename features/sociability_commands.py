import disnake
from disnake.ext import commands
from admin.data_handler import load_data, save_data, ensure_user_profile
from admin.error_log import handle_exception
from Translator.sociability import get_user_language, translations
import re
import os
import json
from datetime import datetime

def setup_profile_socials_commands(bot: commands.Bot):
    @bot.slash_command(name='profile_socials', description=translations["en"]["add_socials"])
    async def profile_socials(inter: disnake.ApplicationCommandInteraction, vkontakte: str = "", telegram: str = "", instagram: str = ""):
        await inter.response.defer()
        print(f"Received VK URL: {vkontakte}, Telegram URL: {telegram}, Instagram URL: {instagram}")

        try:
            user_language = get_user_language(inter)
            locale = translations[user_language]

            user_id = str(inter.author.id)
            data = load_data()
            ensure_user_profile(data, user_id)

            # Проверка валидности URL
            if vkontakte and not validate_vk_url(vkontakte):
                await inter.followup.send(content=locale["invalid_vk"], ephemeral=True)
                return
            if telegram and not validate_telegram_url(telegram):
                await inter.followup.send(content=locale["invalid_telegram"], ephemeral=True)
                return
            if instagram and not validate_instagram_url(instagram):
                await inter.followup.send(content=locale["invalid_instagram"], ephemeral=True)
                return

            # Обновление данных пользователя
            updated = update_user_data(data, user_id, vkontakte, telegram, instagram)
            save_data(data)
            print("Данные после сохранения:", load_data())

            # Подготовка URL аватара (с сервера)
            avatar_url = inter.author.display_avatar.url if inter.author.display_avatar else None

            # Создание элегантного эмбеда с аватаркой и сообщением
            embed = disnake.Embed(
                title=locale["success_message"],
                description=locale["social_updated"] if updated else locale["no_changes"],
            )

            if avatar_url:
                embed.set_thumbnail(url=avatar_url)  # Установка маленькой аватарки пользователя

            await inter.followup.send(embed=embed, ephemeral=True)  # Используйте followup вместо edit_original_response

        except Exception as e:
            print(f"Ошибка: {e}")
            handle_exception(e)

def validate_vk_url(url):
    is_valid = re.match(r'^https://vk\.com/[a-zA-Z0-9._]+/?$', url) is not None
    print(f"VK URL {'is valid' if is_valid else 'is invalid'}: {url}")
    return is_valid

def validate_telegram_url(url):
    is_valid = re.match(r'^https://t\.me/[a-zA-Z0-9._]+/?$', url) is not None
    print(f"Telegram URL {'is valid' if is_valid else 'is invalid'}: {url}")
    return is_valid

def validate_instagram_url(url):
    is_valid = re.match(r'^https://www\.instagram\.com/[a-zA-Z0-9._]+/?$', url) is not None
    print(f"Instagram URL {'is valid' if is_valid else 'is invalid'}: {url}")
    return is_valid

def update_user_data(data, user_id, vkontakte, telegram, instagram):
    updated = False  # Переменная для отслеживания изменений
    if user_id in data:
        user_data = data[user_id]
        if vkontakte:  # Всегда обновляем, если передана ссылка
            user_data["vk"] = vkontakte
            print(f"Updated VK: {vkontakte}")  # Отладка
            updated = True
        if telegram:  # Всегда обновляем, если передана ссылка
            user_data["telegram"] = telegram
            print(f"Updated Telegram: {telegram}")  # Отладка
            updated = True
        if instagram:  # Всегда обновляем, если передана ссылка
            user_data["instagram"] = instagram
            print(f"Updated Instagram: {instagram}")  # Отладка
            updated = True
    else:
        data[user_id] = {
            "status": None,
            "rewards": "0",
            "voice_online": "0 h,0 m",
            "vk": vkontakte,
            "telegram": telegram,
            "instagram": instagram,
            "profile_created": datetime.utcnow().strftime("%d.%m.%Y")
        }
        updated = True  # Установка флага обновления, если новый профиль создан

    return updated

def load_data():
    user_data_path = 'admin/user_data.json'
    if os.path.exists(user_data_path):
        try:
            with open(user_data_path, 'r', encoding='utf-8') as f:  # Указание кодировки
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при загрузке данных: {e}")
            return {}
    else:
        return {}

def save_data(data):
    user_data_path = 'admin/user_data.json'
    try:
        with open(user_data_path, 'w', encoding='utf-8') as f:  # Указание кодировки
            json.dump(data, f, indent=4, ensure_ascii=False)  # Убедитесь, что не используете ASCII
            print("Данные успешно сохранены")
    except IOError as e:
        print(f"Ошибка записи данных пользователя: {e}")








