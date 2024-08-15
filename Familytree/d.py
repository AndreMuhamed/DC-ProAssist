import pickledb
import disnake
from disnake.ext import commands

class Marriage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='divorce', description='Развести с вашим партнёром.')
    async def divorce(self, inter: disnake.ApplicationCommandInteraction):
        author = f"{inter.author.name}#{inter.author.discriminator}"
        db = pickledb.load('Familytree/database.txt', False)
        
        if not db.exists(f"{author}partner"):
            return await inter.send("У вас нет партнёра!")

        target = db.get(f"{author}partner")
        # Удаляем ключи
        db.rem(f"{author}partner")
        db.rem(f"{target}partner")
        db.dump()

        # Уведомляем обоих пользователей
        target_member = inter.guild.get_member(int(target.split('#')[0]))
        if target_member:
            await target_member.send(f"{inter.author.mention} разорвал(а) с вами отношения.")
        
        await inter.send(f"{inter.author.mention}, вы разорвали отношения с {target_member.mention if target_member else target}!")

def setup(bot):
    bot.add_cog(Marriage(bot))

