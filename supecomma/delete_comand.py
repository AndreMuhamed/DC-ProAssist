import disnake
from disnake.ext import commands
import asyncio

class DeleteMessagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Проверяем, что сообщение не от самого бота
        if message.author == self.bot.user:
            return

        # Проверяем, есть ли префикс "!" в сообщении
        if message.content.startswith('!'):
            # Ждем 10 секунд
            await asyncio.sleep(10)
            # Удаляем сообщение
            await message.delete()

def setup(bot):
    bot.add_cog(DeleteMessagesCog(bot))
