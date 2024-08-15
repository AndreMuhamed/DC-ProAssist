import pickledb
import disnake
from disnake.ext import commands
import asyncio

class MarriageCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="marry", description="Предложить руку и сердце другому пользователю")
    async def marry(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        db = pickledb.load('Familytree/database.txt', False)
        author = inter.author

        # Проверка на различные условия
        if member is None:
            return await inter.response.send_message("Пожалуйста, укажите пользователя.", ephemeral=True)
        if member == author:
            return await inter.response.send_message("Вы не можете вступить в брак с самим собой!", ephemeral=True)
        if db.exists(f"{member.name}partner") or db.exists(f"{author.name}partner"):
            return await inter.response.send_message("Либо у вас, либо у выбранного пользователя уже есть партнер!", ephemeral=True)

        # Проверка, не является ли член семьи
        if db.exists(f"{author.name}child"):
            def get_children(parent):
                childlist = []
                for child in db.get(f"{parent}child").split("|/"):
                    if child and db.exists(f"{child}child"):
                        childlist.extend(db.get(f"{child}child").split('|/'))
                        childlist.extend(get_children(child))
                return childlist

            last_child = db.get(f"{author.name}child").split("|/")
            last_child = [child for child in last_child if child]
            for this_child in last_child:
                if db.exists(f"{this_child}child"):
                    last_child.extend(get_children(this_child))
                if member.name in last_child:
                    return await inter.response.send_message("Вы не можете вступить в брак со своим ребенком или внуком!", ephemeral=True)

        # Создание кнопок
        button = disnake.ui.Button(label="Подтвердить", style=disnake.ButtonStyle.green, custom_id="marriage_accept")
        view = disnake.ui.View()
        view.add_item(button)

        # Запросить подтверждение от выбранного пользователя
        question = await inter.response.send_message(
            embed=disnake.Embed(
                title="Предложение о браке",
                description=f"<@{member.id}>, <@{author.id}> предлагает вам вступить в брак!\nНажмите кнопку ниже для подтверждения.",
                color=disnake.Color.blue()
            ),
            view=view
        )

        # Ожидание нажатия кнопки
        def check(interaction: disnake.Interaction):
            return (interaction.type == disnake.InteractionType.component and
                    interaction.custom_id == "marriage_accept" and
                    interaction.user == member)

        try:
            interaction = await self.bot.wait_for('interaction', timeout=450.0, check=check)
            if interaction:
                await interaction.response.send_message("Вы подтвердили предложение о браке!")
                # Сохранить данные о браке
                db.set(f"{author.name}partner", member.name)
                db.set(f"{member.name}partner", author.name)
                db.dump()

        except asyncio.TimeoutError:
            await question.edit(embed=disnake.Embed(
                title="Время истекло",
                description="Период ожидания истек, и предложение о браке не было подтверждено.",
                color=disnake.Color.red()
            ), view=None)

        except Exception as e:
            await inter.followup.send(f'Произошла ошибка: {str(e)}', ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.Interaction):
        # Обрабатываем взаимодействия с кнопками
        if interaction.type == disnake.InteractionType.component:
            if interaction.custom_id == "marriage_accept":
                await interaction.response.send_message("Вы подтвердили предложение о браке!")

def setup(bot):
    bot.add_cog(MarriageCommands(bot))











