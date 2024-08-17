import disnake
from disnake.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="serverinfo", description="Получить информацию о сервере.")
    @commands.cooldown(rate=1, per=10)
    async def serverinfo(self, inter: disnake.ApplicationCommandInteraction):
        guild = inter.guild
        owner = guild.owner
        role_count = len(guild.roles)
        channel_count = len(guild.channels)
        online_members = sum(member.status != disnake.Status.offline for member in guild.members)
        boost_level = guild.premium_tier
        description = guild.description or "Описание отсутствует"

        # Форматирование даты с последними двумя цифрами года
        creation_date = guild.created_at.strftime('%d-%m-%y')

        embed = disnake.Embed(
            title=f"<:Asset1:1274334471532838945> Информация о сервере — {guild.name}!",
        ).set_thumbnail(
            url=guild.icon.url
        ).set_image(
            url="attachment://server_info.gif"
        ).add_field(
            name="> **Название сервера:**", value=f"```{guild.name}```", inline=False
        ).add_field(
            name="> **Описание:**", value=f"```{description}```", inline=False
        ).add_field(
            name="**Всего участников:**", value=f"```{guild.member_count}```"
        ).add_field(
            name="**Участников онлайн:**", value=f"```{online_members}```"
        ).add_field(
            name="**Количество каналов:**", value=f"```{channel_count}```"
        ).add_field(
            name="**Количество ролей:**", value=f"```{role_count}```"
        ).add_field(
            name="**Уровень буста:**", value=f"```{boost_level}```"
        ).add_field(
            name="**Дата создания:**", value=f"```{creation_date}```"
        ).add_field(
            name="> **Владелец сервера:**", value=owner.mention, inline=False
        ).set_footer(
            text="Информация актуальна на момент вызова команды!",
        )

        with open("assets/Инфо.gif", "rb") as gif_file:
            file = disnake.File(gif_file, filename="server_info.gif")
            await inter.response.send_message(embed=embed, file=file)

def setup(bot):
    bot.add_cog(ServerInfo(bot))



