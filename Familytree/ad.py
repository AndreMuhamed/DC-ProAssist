import pickledb
import disnake
from disnake.ext import commands
import asyncio

class AdoptionCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="adopt", description="Усыновить/удочерить пользователя")
    async def adopt(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        author = inter.author
        target = member

        # Открыть базу данных
        db = pickledb.load('Familytree/database.txt', False)

        if target is None:
            return await inter.response.send_message("Пожалуйста, укажите пользователя.", ephemeral=True)
        
        if target == author:
            return await inter.response.send_message("Вы не можете усыновить/удочерить самого себя!", ephemeral=True)
        
        # Проверка, что целевой пользователь не является партнером или уже имеет родителя
        if db.exists(f"{author.name}partner") and target.name == db.get(f"{author.name}partner"):
            return await inter.response.send_message("Вы не можете усыновить/удочерить своего партнера!", ephemeral=True)
        
        if db.exists(f"{target.name}parent"):
            return await inter.response.send_message("У этого пользователя уже есть родитель!", ephemeral=True)

        # Запросить подтверждение от целевого пользователя
        question = await inter.response.send_message(
            f"<@{target.id}>, <@{author.id}> хочет усыновить/удочерить вас!\n"
            f"Отреагируйте ✅ для подтверждения.",
            ephemeral=True
        )
        
        message = await inter.original_message()
        await message.add_reaction('✅')

        def check(reaction, user):
            return user == target and str(reaction.emoji) == '✅'
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await inter.followup.send('Время истекло.', ephemeral=True)
        else:
            if db.exists(f"{target.name}parent"):
                return await inter.followup.send(f"<@{author.id}>, у <@{target.id}> уже есть родитель!", ephemeral=True)
            
            # Обновить базу данных
            if db.exists(f"{author.name}child"):
                existing_children = db.get(f"{author.name}child")
                db.set(f"{author.name}child", existing_children + "|/" + target.name)
            else:
                db.set(f"{author.name}child", target.name)
            
            db.set(f"{target.name}parent", author.name)
            db.dump()

            return await inter.followup.send(f"<@{author.id}>, <@{target.id}> согласился(ась)!", ephemeral=True)

def setup(bot):
    bot.add_cog(AdoptionCommands(bot))

