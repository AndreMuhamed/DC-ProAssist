import disnake
import json
from datetime import datetime, timedelta
from admin.error_log import log_error, handle_exception
from disnake.ext import commands

def setup_rewards_commands(bot: commands.Bot):
    @bot.slash_command(name='reward', description='Получите награду в виде монет.')
    async def reward(inter: disnake.ApplicationCommandInteraction):
        try:
            await inter.response.defer()  # Указываем, что ответ будет позднее
            
            user_id = str(inter.author.id)
            data = load_data()

            if user_id not in data:
                data[user_id] = {"rewards": 0, "last_claim": None}
            
            user_data = data[user_id]

            # Проверка и инициализация ключа rewards
            if 'rewards' not in user_data:
                user_data['rewards'] = 0

            if user_data.get('last_claim'):
                last_claim_date = datetime.fromisoformat(user_data['last_claim'])
                if datetime.utcnow() - last_claim_date < timedelta(hours=12):
                    next_claim_time = last_claim_date + timedelta(hours=12)
                    time_remaining = next_claim_time - datetime.utcnow()
                    hours, remainder = divmod(time_remaining.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)
                    
                    embed = disnake.Embed(
                        title=f"Вознаграждение уже получено — {inter.author.name}",
                        description=f"Вы **уже** получили **вознаграждение!**\n"
                                    f"Вы можете **получить** следующую через **{hours}** ч **{minutes}** мин.",
                    )
                    embed.set_thumbnail(url=inter.author.display_avatar.url if inter.author.display_avatar else inter.author.default_avatar.url)
                    embed.set_footer(text="Спасибо за вашу активность!")

                    # Добавление кнопки "Купить монеты"
                    buy_coins_button = disnake.ui.Button(
                        label="Купить монеты",
                        style=disnake.ButtonStyle.danger,
                        custom_id="buy_coins"
                    )
                    
                    components = [disnake.ui.ActionRow(buy_coins_button)]
                    
                    await inter.followup.send(embed=embed, components=components)
                    return

            user_data['rewards'] += 35  # Пример увеличения вознаграждения
            user_data['last_claim'] = datetime.utcnow().isoformat()
            data[user_id] = user_data
            save_data(data)

            embed = disnake.Embed(
                title=f"Вознаграждение получено — {inter.author.name}",
                description=f"Вы получили вознаграждение в сумме **35** монет.\n"
                            f"Теперь у вас в профиле **{user_data['rewards']}** монет.",
            )
            embed.set_thumbnail(url=inter.author.display_avatar.url if inter.author.display_avatar else inter.author.default_avatar.url)
            embed.set_footer(text="Спасибо за вашу активность!")

            # Добавление кнопки "Купить монеты"
            buy_coins_button = disnake.ui.Button(
                label="Купить монеты",
                style=disnake.ButtonStyle.danger,
                custom_id="buy_coins"
            )
            
            components = [disnake.ui.ActionRow(buy_coins_button)]

            await inter.followup.send(embed=embed, components=components)
        
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

def load_data():
    try:
        with open('admin/user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        handle_exception(e)
        return {}

def save_data(data):
    try:
        with open('admin/user_data.json', 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        handle_exception(e)
        print(f"Ошибка записи данных пользователя: {e}")

def ensure_user_profile(data, user_id):
    if user_id not in data:
        data[user_id] = {
            "status": "Нет статуса",
            "rewards": 0,
            "voice_online": "0 ч, 0 м",
            "vk": "Не указано",
            "telegram": "Не указано",
            "instagram": "Не указано",
            "profile_created": datetime.utcnow().strftime("%d.%m.%Y")
        }















