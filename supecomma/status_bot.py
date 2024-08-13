import disnake
from disnake.ext import commands, tasks

class StatusBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status_list = [
            "YouTube: Game Quest", "YouTube: Nanson", "YouTube: ANIME INDUSTRY", "YouTube: KINO INDUSTRY", "YouTube: Стримус", 
            
            "andremuhamed.nexcord.pro"
        ]
        self.current_status = 0
        self.status_task.start()

    @tasks.loop(minutes=5)
    async def status_task(self):
        """Циклическое изменение статуса бота."""
        status_name = self.status_list[self.current_status]
        await self.bot.change_presence(status=disnake.Status.dnd, activity=disnake.Activity(type=disnake.ActivityType.watching, name=status_name))
        
        # Переключаем статус
        self.current_status = (self.current_status + 1) % len(self.status_list)

    @status_task.before_loop
    async def before_status_task(self):
        """Ожидаем, пока бот станет доступным."""
        await self.bot.wait_until_ready()

def setup(bot: commands.Bot):
    bot.add_cog(StatusBot(bot))
        


