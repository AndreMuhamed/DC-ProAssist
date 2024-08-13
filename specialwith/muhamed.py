import disnake
from disnake.ext import commands

class Muhamed(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='создатель')
    async def creator(self, ctx: commands.Context):
        await ctx.send("Большой ХУЙ")

    @commands.command(name='иван')
    async def иван(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Иван - настоящий герой!",
            description="В игре Иван всегда готов к вызовам и битвам. Но даже сильному воину нужно поддерживать силу, чтобы продолжать свое подвигание!",
        )
        await ctx.send(embed=embed)

    @commands.command(name='hezuko')
    async def hezuko(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Hezuko - верный друг и опора",
            description="Nezuko - это не только красивая девушка, но и большая опора и верный друг. Ее вера в успех проекта всегда вдохновляла нас и помогала преодолевать любые трудности.",
        )
        await ctx.send(embed=embed)

    @commands.command(name='эдвард')
    async def эдвард(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Сердечная благодарность Эдварду",
            description="Сердечная благодарность Эдварду за его неизменную поддержку и значительный вклад в разработку дискорд-бота. Его экспертиза и навыки были неоценимы в этом процессе, и мы бесконечно признательны за его преданность и профессионализм. Пусть он получит заслуженное уважение за свой вклад в наш проект!",
        )
        await ctx.send(embed=embed)

    @commands.command(name='сахарок')
    async def сахарок(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Сладкий сахарок",
            description="Она настолько сладкая, что ты ее захочешь попробовать даже в игре, потому что сахар - это энергия!",
        )
        await ctx.send(embed=embed)

    @commands.command(name='солнышко')
    async def солнышко(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Привет от солнышка!",
            description="Обожает объятия, погружается в игры настолько глубоко, что поднимает настроение всем друзьям. При этом много спит, но когда просыпается, создает уютную атмосферу вокруг себя!",
        )
        await ctx.send(embed=embed)

    @commands.command(name='романджи')
    async def солнышко(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Интересный парень — RomanJ",
            description="Добрый, умный, мечтает о большем, хочет быть самым умным и красивым как фембой. Ну вот...",
        )
        await ctx.send(embed=embed)    

def setup(bot: commands.Bot):
    bot.add_cog(Muhamed(bot))