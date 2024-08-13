import json
import disnake
from disnake.ext import commands

def setup_rich_users(bot: commands.Bot):
    @bot.slash_command(name='top_rich', description='Показать рейтинг самых богатых пользователей.')
    async def top_rich(inter: disnake.ApplicationCommandInteraction):
        data = load_user_data()
        sorted_users = sorted(
            [(user_id, user_data) for user_id, user_data in data.items() if user_id.isdigit()],
            key=lambda x: x[1].get('rewards', 0),
            reverse=True
        )
        
        if not sorted_users:
            await inter.send("Нет данных о пользователях.")
            return

        embed = disnake.Embed(title="Рейтинг самых богатых пользователей:")
        for i, (user_id, user_data) in enumerate(sorted_users[:10], start=1):  # Топ-10 пользователей
            rewards = user_data.get('rewards', 0)
            user = bot.get_user(int(user_id))
            username = user.name if user else 'Не найдено'
            embed.add_field(name=f"{i}. {username}", value=f"{rewards} монет", inline=False)
        
        await inter.send(embed=embed)

    def load_user_data():
        try:
            with open('admin/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


