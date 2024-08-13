import disnake
from disnake.ext import commands
from disnake.ui import Button, View

class Individual(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def create_order_button(self):
        # Используем стиль danger для красной кнопки
        button = Button(style=disnake.ButtonStyle.danger, label="Заказать команду", custom_id="order_command")
        view = View()
        view.add_item(button)
        return view

    @commands.command(name='individ')
    async def индивидуальная(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Индивидуальная команда уже тут!",
            description="```Эта команда отправляет индивидуальное сообщение в виде embed с указанным текстом заказчика.```",
        )
        # Убедитесь, что у бота есть аватар
        avatar_url = self.bot.user.avatar.url if self.bot.user.avatar else 'https://cdn.discordapp.com/embed/avatars/0.png'
        embed.set_footer(
            text="Благодарим за использование наших сервисов!",
            icon_url=avatar_url
        )
        
        view = self.create_order_button()
        await ctx.send(embed=embed, view=view)

    @commands.command(name='another_command')
    async def another_command(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Еще одна команда!",
            description="```Эта команда также отправляет сообщение с кнопкой заказа команды.```",
        )
        # Убедитесь, что у бота есть аватар
        avatar_url = self.bot.user.avatar.url if self.bot.user.avatar else 'https://cdn.discordapp.com/embed/avatars/0.png'
        embed.set_footer(
            text="Благодарим за использование наших сервисов!",
            icon_url=avatar_url
        )
        
        view = self.create_order_button()
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: disnake.MessageInteraction):
        if interaction.component.custom_id == "order_command":
            seller_avatar_url = "https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png"
            
            # Создание эмбеда для отправки сообщения
            embed = disnake.Embed(
                title="<:Stickerus8:1269746123673960663> Покупка комады в Online Shop!",
                description="Спасибо за интерес к покупке команды! Для завершения покупки, пожалуйста, свяжитесь с продавцом.",
            )
            embed.add_field(
                name="Ссылка на продавцов:",
                value="<@768782555171782667> или <@787093771115692062>"
            )
            embed.set_thumbnail(url=seller_avatar_url)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Individual(bot))

      
