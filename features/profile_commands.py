import disnake  
from disnake.ext import commands
from admin.data_handler import load_data, save_data, ensure_user_profile
from admin.error_log import handle_exception
from Translator.profile import get_user_language, translations
import re


def setup_profile_commands(bot: commands.Bot):
    @bot.slash_command(name='profile', description=translations["en"]["view_profile"])
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








