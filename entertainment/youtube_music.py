import disnake
from disnake.ext import commands
import yt_dlp as youtube_dl

# Настройки для yt-dlp
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,  # Не загружать плейлисты
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def play_music(self, interaction: disnake.ApplicationCommandInteraction):
        """Проигрывание музыки с YouTube."""
        # Отложенный ответ на взаимодействие
        await interaction.response.defer()

        # Подключение бота к голосовому каналу пользователя
        voice_channel = interaction.author.voice.channel
        if not voice_channel:
            await interaction.followup.send("Вы должны находиться в голосовом канале, чтобы воспроизвести музыку.", ephemeral=True)
            return
        
        voice_client = await voice_channel.connect()

        url = "https://youtu.be/gXTfxIEqH-E"  # Укажите ссылку на YouTube
        try:
            # Получение информации о видео
            info = ytdl.extract_info(url, download=False)
            print(info)  # Отладочный вывод для проверки структуры данных

            # Попытка получить URL для воспроизведения
            url2 = info.get('url') or info.get('webpage_url')
            if not url2:
                raise KeyError("URL не найден в данных.")

            # Проигрывание музыки
            voice_client.play(disnake.FFmpegPCMAudio(executable="ffmpeg", source=url2))
            await interaction.followup.send(f"Сейчас играет: {info['title']}")

        except KeyError:
            # Обработка ситуации, если URL не найден
            await interaction.followup.send("Не удалось получить URL для воспроизведения видео.", ephemeral=True)
            return
        except Exception as e:
            # Общая обработка исключений
            await interaction.followup.send(f"Произошла ошибка: {str(e)}", ephemeral=True)
            return

    @commands.slash_command()
    async def stop_music(self, interaction: disnake.ApplicationCommandInteraction):
        """Остановить воспроизведение музыки."""
        # Остановка воспроизведения и отключение от канала
        if interaction.guild.voice_client:  # Проверяем, подключён ли бот к голосовому каналу
            await interaction.guild.voice_client.disconnect()
            await interaction.followup.send("Музыка остановлена и бот отключён от голосового канала.")
        else:
            await interaction.followup.send("Бот не подключён к голосовому каналу.", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))


