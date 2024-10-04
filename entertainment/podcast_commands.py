import disnake
from disnake.ext import commands
import yt_dlp as youtube_dl
import sys
import io
import random
import asyncio
from Translator.podcast import translations, get_user_language  # Импортируем переводы и функцию

# Устанавливаем кодировку UTF-8 для вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Настройки для yt-dlp
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,  # Не загружать плейлисты
    'retries': 5,  # Число попыток при сетевых сбоях
    'http_chunk_size': 1048576,  # Деление загрузки на куски (1MB)
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Список URL'ов видео
video_urls = [
    "https://youtu.be/1POB1e32ByI",
    "https://youtu.be/h2kCkHc3zFQ",
    "https://youtu.be/KiaenZaYaQ0"
]

class Podcast(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Podcasts from commander Andrey Muhameda.')
    async def play_podcast(self, interaction: disnake.ApplicationCommandInteraction):
        """Проигрывание музыки с YouTube."""
        try:
            await interaction.response.defer()  # Деферируем ответ, пока выполняем код
            
            user_lang = get_user_language(interaction)  # Определяем язык пользователя
            lang = translations[user_lang]  # Получаем соответствующие переводы

            voice_channel = interaction.author.voice.channel if interaction.author.voice else None
            if not voice_channel:
                await interaction.followup.send(lang["must_be_in_voice"], ephemeral=True)
                return

            voice_client = await voice_channel.connect()

            # Выбираем случайное видео
            video_url = random.choice(video_urls)

            # Создание эмбеда
            embed = disnake.Embed(
                title=lang["listen_podcast"],
                description=lang["interesting_today"]
            )

            # Добавление изображения в эмбед
            embed.set_image(url="https://cdn.discordapp.com/attachments/963534892082290688/1267128077117292655/FaS7iOhBBW0.jpg")
            embed.set_footer(text=lang["footer_text"])  # Текст подвала

            # Отправляем сообщение с эмбедом
            await interaction.followup.send(embed=embed)

            # Проигрывание музыки
            await self.start_playing(voice_client, video_url, interaction, lang)

            # Устанавливаем таймер на 35 секунд
            await asyncio.sleep(35)
            await voice_client.disconnect()

        except Exception as e:
            # Ловим любые исключения и отправляем сообщение об ошибке
            print(f"Interaction error: {str(e)}")
            await interaction.followup.send(f"{lang['error_occurred']}: {str(e)}", ephemeral=True)

    async def start_playing(self, voice_client, url, interaction, lang):
        """Начинает воспроизведение трека с YouTube."""
        try:
            info = ytdl.extract_info(url, download=False)
            url2 = info.get('url') or info.get('webpage_url')
            if not url2:
                await interaction.followup.send(lang["stream_error"], ephemeral=True)
                return

            # Используем FFmpeg для проигрывания потока
            voice_client.play(disnake.FFmpegPCMAudio(executable="ffmpeg", source=url2))

        except Exception as e:
            print(f"Exception: {str(e)}")  # Логирование ошибки для отладки
            await interaction.followup.send(f"{lang['error_occurred']}: {str(e)}", ephemeral=True)
            await voice_client.disconnect()  # Переподключение в случае ошибки

def setup(bot: commands.Bot):
    bot.add_cog(Podcast(bot))





