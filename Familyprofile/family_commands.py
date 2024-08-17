import disnake
from disnake.ext import commands
import json

class MarriageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pending_marriages = {}  # Для хранения запросов на брак

    @commands.slash_command(name='брак', description='Управление браками.')
    async def marriage(self, inter: disnake.ApplicationCommandInteraction, действие: str = commands.Param(choices=["создать", "информация", "история", "развестись"]), пользователь: disnake.Member = None):
        if действие == "создать":
            if пользователь:
                await self.request_marriage(inter, пользователь)
            else:
                embed = disnake.Embed(description="Пожалуйста, выберите пользователя для создания брака.", color=disnake.Color.red())
                await inter.send(embed=embed, ephemeral=True)
        elif действие == "информация":
            await self.get_marriage_info(inter, пользователь)
        elif действие == "история":
            await self.get_marriage_history(inter)
        elif действие == "развестись":
            await self.divorce(inter)

    async def request_marriage(self, inter: disnake.ApplicationCommandInteraction, пользователь: disnake.Member):
        data = self.load_marriage_data()
        balance_data = self.load_user_data()
        user_id = str(inter.author.id)

        # Проверка баланса пользователя
        if user_id not in balance_data or balance_data[user_id].get("rewards", 0) < 2500:
            embed = disnake.Embed(description="У вас недостаточно средств для создания брака. Требуется 2500 монет.", color=disnake.Color.red())
            await inter.send(embed=embed, ephemeral=True)
            return

        # Проверка, не состоит ли пользователь уже в браке
        if user_id in data and data[user_id].get("married_to"):
            embed = disnake.Embed(description=f"Вы уже состоите в браке с {data[user_id]['married_to']}.", color=disnake.Color.red())
            await inter.send(embed=embed, ephemeral=True)
            return

        partner_id = str(пользователь.id)
        if partner_id in data and data[partner_id].get("married_to"):
            embed = disnake.Embed(description=f"{пользователь.mention} уже состоит в браке.", color=disnake.Color.red())
            await inter.send(embed=embed, ephemeral=True)
            return

        # Запрос на подтверждение брака
        self.pending_marriages[partner_id] = user_id

        embed = disnake.Embed(
            title="Запрос на брак",
            description=f"{пользователь.mention}, {inter.author.mention} хочет вступить с вами в брак. Подтвердите или отклоните запрос.",
            color=disnake.Color.blue()
        )
        await inter.send(embed=embed, ephemeral=True)
        await пользователь.send(embed=embed)

    async def create_marriage(self, inter: disnake.ApplicationCommandInteraction, партнер: disnake.Member):
        data = self.load_marriage_data()
        balance_data = self.load_user_data()
        user_id = str(inter.author.id)
        partner_id = str(партнер.id)

        data[user_id] = {
            "married_to": partner_id,
            "date": inter.created_at.isoformat()
        }
        data[partner_id] = {
            "married_to": user_id,
            "date": inter.created_at.isoformat()
        }

        # Списание средств
        balance_data[user_id]["rewards"] -= 2500
        self.save_user_data(balance_data)
        self.save_marriage_data(data)

        # Добавление в историю
        self.update_marriage_history(user_id, partner_id, "создание брака")

        embed = disnake.Embed(
            title="Поздравляем!",
            description=f"{inter.author.mention} и {партнер.mention} теперь состоят в браке! С вашего счёта снято 2500 монет.",
            color=disnake.Color.green()
        )
        await inter.send(embed=embed)
        await партнер.send(embed=embed)

    async def get_marriage_info(self, inter: disnake.ApplicationCommandInteraction, пользователь: disnake.Member = None):
        data = self.load_marriage_data()
        if пользователь:
            user_id = str(пользователь.id)
        else:
            user_id = str(inter.author.id)

        if user_id in data and data[user_id].get("married_to"):
            partner_id = data[user_id]["married_to"]
            partner = inter.guild.get_member(int(partner_id))
            marriage_date = data[user_id].get("date")
            partner_name = partner.mention if partner else f"<@{partner_id}>"
            embed = disnake.Embed(
                title="Информация о браке",
                description=f"{пользователь.mention if пользователь else 'Вы'} состоите в браке с {partner_name} с {marriage_date}.",
                color=disnake.Color.blue()
            )
            await inter.send(embed=embed)
        else:
            embed = disnake.Embed(
                description=f"{пользователь.mention if пользователь else 'Вы'} не состоите в браке.",
                color=disnake.Color.red()
            )
            await inter.send(embed=embed)

    async def get_marriage_history(self, inter: disnake.ApplicationCommandInteraction):
        history = self.load_marriage_history()
        user_id = str(inter.author.id)

        if user_id in history:
            embed = disnake.Embed(
                title="История браков",
                description="\n".join(history[user_id]),
                color=disnake.Color.blue()
            )
            await inter.send(embed=embed)
        else:
            embed = disnake.Embed(
                description="У вас нет истории браков.",
                color=disnake.Color.red()
            )
            await inter.send(embed=embed)

    async def divorce(self, inter: disnake.ApplicationCommandInteraction):
        data = self.load_marriage_data()
        user_id = str(inter.author.id)

        if user_id in data and data[user_id].get("married_to"):
            partner_id = data[user_id]["married_to"]
            partner = inter.guild.get_member(int(partner_id))
            partner_name = partner.mention if partner else f"<@{partner_id}>"

            # Удаление данных о браке
            del data[user_id]
            del data[partner_id]

            self.save_marriage_data(data)

            # Обновление истории
            self.update_marriage_history(user_id, partner_id, "развод")

            embed = disnake.Embed(
                title="Развод",
                description=f"{inter.author.mention} и {partner_name} больше не состоят в браке.",
                color=disnake.Color.orange()
            )
            await inter.send(embed=embed)
            await partner.send(embed=embed)
        else:
            embed = disnake.Embed(
                description="Вы не состоите в браке.",
                color=disnake.Color.red()
            )
            await inter.send(embed=embed)

    def load_marriage_data(self):
        try:
            with open('admin/marriage_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_marriage_data(self, data):
        with open('admin/marriage_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def load_user_data(self):
        try:
            with open('admin/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_user_data(self, data):
        with open('admin/user_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def load_marriage_history(self):
        try:
            with open('admin/marriage_history.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_marriage_history(self, history):
        with open('admin/marriage_history.json', 'w') as f:
            json.dump(history, f, indent=4)

    def update_marriage_history(self, user_id, partner_id, action):
        history = self.load_marriage_history()
        if user_id not in history:
            history[user_id] = []
        if partner_id not in history:
            history[partner_id] = []
        
        entry = f"{action.capitalize()} с {partner_id} ({action} {self.bot.user.name})"
        history[user_id].append(entry)
        history[partner_id].append(entry)

        self.save_marriage_history(history)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id.startswith("marriage_accept_"):
            partner_id = inter.component.custom_id.split("_")[-1]
            if partner_id in self.pending_marriages:
                await self.create_marriage(inter, inter.guild.get_member(int(partner_id)))
                del self.pending_marriages[partner_id]
            else:
                embed = disnake.Embed(description="Запрос на брак устарел.", color=disnake.Color.red())
                await inter.send(embed=embed, ephemeral=True)
        elif inter.component.custom_id.startswith("marriage_decline_"):
            partner_id = inter.component.custom_id.split("_")[-1]
            if partner_id in self.pending_marriages:
                embed = disnake.Embed(description="Запрос на брак отклонён.", color=disnake.Color.red())
                await inter.send(embed=embed, ephemeral=True)
                del self.pending_marriages[partner_id]

def setup(bot):
    bot.add_cog(MarriageCommands(bot))

