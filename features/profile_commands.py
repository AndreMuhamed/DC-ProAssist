import disnake  
from disnake.ext import commands
from admin.data_handler import load_data, save_data, ensure_user_profile
from admin.error_log import handle_exception
from Translator.profile import get_user_language, translations
import re
import os
import json
from datetime import datetime


def setup_profile_commands(bot: commands.Bot):
    @bot.slash_command(name='profile', description=translations["en"]["view_profile"])  # Описание на русском по умолчанию
    async def profile(inter: disnake.ApplicationCommandInteraction, пользователь: disnake.User = None):
        await inter.response.defer()

        # Получаем язык пользователя
        user_language = get_user_language(inter)
        # Берем переводы для конкретного языка
        locale = translations[user_language]

        try:
            user = пользователь or inter.author
            user_id = str(user.id)
            data = load_data()  
            ensure_user_profile(data, user_id)  

            user_data = data.get(user_id, {})
            avatar_url = user.display_avatar.url if user.display_avatar else user.default_avatar.url
            status = user_data.get('status', locale.get("no_status"))  # Используем перевод
            rewards = user_data.get('rewards', 0)
            voice_online = user_data.get('voice_online', locale["no_voice_time"])  # Используем перевод
            vk = user_data.get('vk', locale["not_provided"])  # Используем перевод
            telegram = user_data.get('telegram', locale["not_provided"])  # Используем перевод
            instagram = user_data.get('instagram', locale["not_provided"])  # Используем перевод
            profile_created = user_data.get('profile_created', locale["not_provided"])  # Используем перевод

            embed = disnake.Embed(
                title=locale["profile_title"].format(user=user.name),
                description=f"> **{locale['status']}:**\n```{status}```",
            )
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name=f"> **{locale['coins']}:**", value=f"```{rewards}```", inline=True)
            embed.add_field(name=f"> **{locale['voice_online']}:**", value=f"```{voice_online}```", inline=True)
            embed.add_field(name=f"> **{locale['profile_created']}:**", value=f"```{profile_created}```", inline=True)

            buttons = []
            if vk != locale["not_provided"]:
                buttons.append(disnake.ui.Button(label="VKontakte", url=vk))
            if telegram != locale["not_provided"]:
                buttons.append(disnake.ui.Button(label="Telegram", url=telegram))
            if instagram != locale["not_provided"]:
                buttons.append(disnake.ui.Button(label="Instagram", url=instagram))

            buy_coins_button = disnake.ui.Button(
                label=locale["buy_coins"],
                style=disnake.ButtonStyle.danger,
                custom_id="buy_coins"
            )

            components = [disnake.ui.ActionRow(*buttons, buy_coins_button)] if buttons else [disnake.ui.ActionRow(buy_coins_button)]

            await inter.edit_original_response(embed=embed, components=components)
        
        except Exception as e:
            handle_exception(e)

    @bot.listen("on_button_click")
    async def on_button_click(interaction: disnake.MessageInteraction):
        try:
            user_language = get_user_language(interaction)
            locale = translations[user_language]  # Используем переводы для кнопки

            if interaction.component.custom_id == "buy_coins":
                seller_avatar_url = "https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png"
                
                embed = disnake.Embed(
                    title="<:Stickerus8:1269746123673960663> " + locale["buy_coins_title"],
                    description=locale["buy_coins_description"],
                )
                embed.add_field(
                    name=locale["seller_link_title"],
                    value="<@768782555171782667> или <@787093771115692062>"
                )
                embed.set_thumbnail(url=seller_avatar_url)
                
                await interaction.send(embed=embed, ephemeral=True)
    
        except Exception as e:
            handle_exception(e)

    @bot.slash_command(name='profile_socials', description=translations["en"]["add_socials"])  # Описание на русском по умолчанию
    async def profile_socials(inter: disnake.ApplicationCommandInteraction, vkontakte: str = "", telegram: str = "", instagram: str = ""):
        await inter.response.defer()

        try:
            user_language = get_user_language(inter)
            locale = translations[user_language]  # Используем переводы для конкретного языка

            user_id = str(inter.author.id)
            data = load_data()  
            ensure_user_profile(data, user_id)  

            if vkontakte and not validate_vk_url(vkontakte):
                await inter.edit_original_response(content=locale["invalid_vk"], ephemeral=True)
                return
            if telegram and not validate_telegram_url(telegram):
                await inter.edit_original_response(content=locale["invalid_telegram"], ephemeral=True)
                return
            if instagram and not validate_instagram_url(instagram):
                await inter.edit_original_response(content=locale["invalid_instagram"], ephemeral=True)
                return

            update_user_data(data, user_id, vkontakte, telegram, instagram)
            save_data(data)
            await inter.edit_original_response(content=locale["social_updated"], ephemeral=True)
        
        except Exception as e:
            handle_exception(e)

def validate_vk_url(url):
    return re.match(r'^https://vk\.com/\w+$', url)

def validate_telegram_url(url):
    return re.match(r'^https://t\.me/\w+$', url)

def validate_instagram_url(url):
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
            "status": translations["ru"]["no_status"],  # Используем перевод на русском по умолчанию
            "rewards": 0,
            "voice_online": translations["ru"]["no_voice_time"],
            "vk": vkontakte or translations["ru"]["not_provided"],
            "telegram": telegram or translations["ru"]["not_provided"],
            "instagram": instagram or translations["ru"]["not_provided"],
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







