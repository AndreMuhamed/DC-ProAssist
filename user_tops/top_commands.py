import json
import disnake
from disnake.ext import commands

class TopCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='top', description='Показать рейтинг пользователей.')
    async def top(self, inter: disnake.ApplicationCommandInteraction, по: str = commands.Param(choices=["балансу", "онлайну"])):
        if по == "балансу":
            await self.show_top_rich(inter)
        elif по == "онлайну":
            await self.show_top_voice(inter)

    async def show_top_rich(self, inter: disnake.ApplicationCommandInteraction):
        data = self.load_user_data()
        sorted_users = sorted(
            [(user_id, user_data) for user_id, user_data in data.items() if user_id.isdigit()],
            key=lambda x: x[1].get('rewards', 0),
            reverse=True
        )
        
        if not sorted_users:
            await inter.send("Нет данных о пользователях.")
            return

        embed = disnake.Embed(
            title="<:Stickerus9:1269746132070826075> Рейтинг самых богатых пользователей!",
        )

        for i, (user_id, user_data) in enumerate(sorted_users[:10], start=1):
            rewards = user_data.get('rewards', 0)
            member = inter.guild.get_member(int(user_id))
            if member:
                username = member.mention
            else:
                username = f'Не найдено <@{user_id}>'

            embed.add_field(
                name=f"{i}. {username} — {rewards} монет",
                value=f"",
                inline=False
            )

        embed.set_thumbnail(url=inter.author.display_avatar.url)
        embed.set_footer(text="Спасибо за вашу активность!")
        await inter.send(embed=embed)

    async def show_top_voice(self, inter: disnake.ApplicationCommandInteraction):
        data = self.load_voice_data()
        sorted_users = sorted(
            [(user_id, user_data) for user_id, user_data in data.items() if user_id.isdigit()],
            key=lambda x: self.convert_to_seconds(x[1].get('voice_online', 0)),
            reverse=True
        )
        
        if not sorted_users:
            await inter.send("Нет данных о пользователях.")
            return

        embed = disnake.Embed(
            title="<:Stickerus9:1269746132070826075> Рейтинг самых общительных пользователей!",
        )

        for i, (user_id, user_data) in enumerate(sorted_users[:10], start=1):
            seconds = self.convert_to_seconds(user_data.get('voice_online', 0))
            formatted_time = self.format_seconds(seconds)
            member = inter.guild.get_member(int(user_id))
            if member:
                username = member.mention
            else:
                username = f'Не найдено <@{user_id}>'

            embed.add_field(
                name=f"{i}. {username} — {formatted_time}",
                value=f"",
                inline=False
            )

        embed.set_thumbnail(url=inter.author.display_avatar.url)
        embed.set_footer(text="Спасибо за вашу активность!")
        await inter.send(embed=embed)

    def load_user_data(self):
        try:
            with open('admin/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def load_voice_data(self):
        try:
            with open('admin/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def format_seconds(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours} часов, {minutes} минут"

    def convert_to_seconds(self, time_str):
        if isinstance(time_str, int):
            return time_str
        if isinstance(time_str, str):
            parts = time_str.split(' ч, ')
            if len(parts) == 2:
                hours = int(parts[0])
                minutes = int(parts[1].replace(' м', ''))
                return hours * 3600 + minutes * 60
        return 0

def setup(bot):
    bot.add_cog(TopCommands(bot))


