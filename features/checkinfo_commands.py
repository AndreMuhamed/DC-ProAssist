import disnake
from disnake.ext import commands
from disnake.ui import Button, View
import json

class CheckInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='know', description='Узнать баланс, голосовой онлайн или транзакции.')
    async def узнать(
        self,
        inter: disnake.ApplicationCommandInteraction,
        что: str = commands.Param(choices=["Баланс", "Голосовой онлайн", "Транзакции"]),
        пользователь: disnake.Member = None
    ):
        пользователь = пользователь or inter.author
        пользователь_id = str(пользователь.id)
        data = load_data()

        profile_created = data.get(пользователь_id, {}).get('profile_created', 'Неизвестно')

        # Инициализируем переменную view
        view = None

        if что == "Баланс":
            embed = disnake.Embed(
                title=f"Текущий баланс пользователя — {пользователь.name}"
            )
            баланс = data.get(пользователь_id, {}).get('rewards', 0)
            embed.add_field(name="> Монеты:", value=f"```{баланс}```", inline=True)
            embed.add_field(name="> Создан профиль:", value=f"```{profile_created}```", inline=True)

        elif что == "Голосовой онлайн":
            embed = disnake.Embed(
                title=f"Голосовой онлайн пользователя — {пользователь.name}"
            )
            голосовой_онлайн = data.get(пользователь_id, {}).get('voice_online', 0)
            embed.add_field(name="> Голосовой онлайн:", value=f"```{голосовой_онлайн}```", inline=True)
            embed.add_field(name="> Создан профиль:", value=f"```{profile_created}```", inline=True)

        elif что == "Транзакции":
            транзакции = data.get(пользователь_id, {}).get('transactions', [])
            if транзакции:
                embed = await self.create_transaction_embed(пользователь, транзакции, 0)
                view = self.create_pagination_view(пользователь, транзакции, 0)
            else:
                embed = disnake.Embed(
                    title=f"Транзакции пользователя — {пользователь.name}",
                    description="У пользователя нет транзакций."
                )

        # Добавление аватарки пользователя
        серверный_аватар = пользователь.guild_avatar.url if пользователь.guild_avatar else пользователь.display_avatar.url
        embed.set_thumbnail(url=серверный_аватар)

        if view:  # Отправляем view только если он не None
            await inter.send(embed=embed, view=view)
        else:
            await inter.send(embed=embed)

    async def create_transaction_embed(self, пользователь, транзакции, page):
        start_index = page * 10
        end_index = min(start_index + 10, len(транзакции))
        транзакции_текст = "\n".join([f"- {t}" for t in транзакции[start_index:end_index]])
        embed = disnake.Embed(
            title=f"Транзакции пользователя — {пользователь.name}",
            description=f"{транзакции_текст}",
        )
        return embed

    def create_pagination_view(self, пользователь, транзакции, current_page):
        view = View()

        if current_page > 0:
            prev_button = Button(label="⏪ Предыдущая", style=disnake.ButtonStyle.secondary, custom_id=f"prev_{пользователь.id}_{current_page - 1}")
            view.add_item(prev_button)

        if len(транзакции) > (current_page + 1) * 10:
            next_button = Button(label="⏩ Следующая", style=disnake.ButtonStyle.secondary, custom_id=f"next_{пользователь.id}_{current_page + 1}")
            view.add_item(next_button)

        return view

    @commands.Cog.listener()
    async def on_interaction(self, inter: disnake.Interaction):
        if inter.type == disnake.InteractionType.component:
            custom_id = inter.data.get('custom_id')
            if custom_id and custom_id.startswith(('prev_', 'next_')):
                parts = custom_id.split('_')
                action = parts[0]
                пользователь_id = parts[1]
                page = int(parts[2])

                # Загрузка данных и транзакций пользователя
                data = load_data()
                транзакции = data.get(пользователь_id, {}).get('transactions', [])
                пользователь = await self.bot.fetch_user(пользователь_id)

                embed = await self.create_transaction_embed(пользователь, транзакции, page)
                view = self.create_pagination_view(пользователь, транзакции, page)

                await inter.response.edit_message(embed=embed, view=view)

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

def setup(bot):
    bot.add_cog(CheckInfo(bot))