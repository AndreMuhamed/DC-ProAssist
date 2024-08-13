import disnake
from disnake.ext import commands
from supecomma.config import Channel_ids, REMINDER_CHANNEL_IDS

class ReminderSender:
    def __init__(self, bot):
        self.bot = bot
        self.message_counts = {channel_id: 0 for channel_id in Channel_ids}

    async def send_reminders(self):
        for reminder_channel_id in REMINDER_CHANNEL_IDS:
            reminder_channel = self.bot.get_channel(reminder_channel_id)
            if reminder_channel:
                embed = disnake.Embed(
                    title="<:Stickerus5:1269746098809864232> Напоминание о проектах!",
                    description=(
                        "Хотим напомнить **вам**, что у **Андрея Мухамеда** есть замечательные **проекты** на YouTube, а также личный веб-сайт.\n"
                        "Если вам интересно, можете перейти **по кнопкам** ниже, чтобы узнать больше!"
                    ),
                )

                with open('assets/vacation.gif', 'rb') as f:
                    file = disnake.File(f, filename='vacation.gif')
                    embed.set_image(url='attachment://vacation.gif')

                button_row = disnake.ui.ActionRow(
                    disnake.ui.Button(label="Website Muhameda", style=disnake.ButtonStyle.link, url="https://andremuhamed.nexcord.pro/language/home_ru"),
                    disnake.ui.Button(label="Multilink", style=disnake.ButtonStyle.link, url="https://andremuhamed.nexcord.pro/multilink/creator/torex")
                )

                await reminder_channel.send(embed=embed, file=file, components=[button_row])
                
                # Сбросить счётчик сообщений только для текущего канала
                self.message_counts = {channel_id: 0 for channel_id in self.message_counts if channel_id == reminder_channel_id}

    async def on_message(self, message):
        if message.channel.id in self.message_counts:
            self.message_counts[message.channel.id] += 1
            if self.message_counts[message.channel.id] >= 600:
                await self.send_reminders()

def setup(bot):
    bot.reminder_sender = ReminderSender(bot)
    bot.add_listener(bot.reminder_sender.on_message, "on_message")

