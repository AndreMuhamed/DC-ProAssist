import json
import disnake
from disnake.ext import commands

def setup_sociable_users(bot: commands.Bot):
    @bot.slash_command(name='top_voice', description='Показать рейтинг самых общительных пользователей.')
    async def top_voice(inter: disnake.ApplicationCommandInteraction):
        data = load_voice_data()
        sorted_users = sorted(
            [(user_id, user_data) for user_id, user_data in data.items() if user_id.isdigit()],
            key=lambda x: convert_to_seconds(x[1].get('voice_online', 0)),
            reverse=True
        )
        
        if not sorted_users:
            await inter.send("Нет данных о пользователях.")
            return

        embed = disnake.Embed(title="Рейтинг самых общительных пользователей:")
        for i, (user_id, user_data) in enumerate(sorted_users[:10], start=1):  # Топ-10 пользователей
            seconds = convert_to_seconds(user_data.get('voice_online', 0))
            formatted_time = format_seconds(seconds)
            user = bot.get_user(int(user_id))
            username = user.name if user else 'Не найдено'
            embed.add_field(name=f"{i}. {username}", value=f"{formatted_time}", inline=False)
        
        await inter.send(embed=embed)

    def load_voice_data():
        try:
            with open('admin/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def format_seconds(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours} ч, {minutes} м"

    def convert_to_seconds(time_str):
        if isinstance(time_str, int):
            return time_str
        if isinstance(time_str, str):
            parts = time_str.split(' ч, ')
            if len(parts) == 2:
                hours = int(parts[0])
                minutes = int(parts[1].replace(' м', ''))
                return hours * 3600 + minutes * 60
        return 0
