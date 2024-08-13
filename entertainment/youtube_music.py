import disnake
from disnake.ext import commands, tasks
import yt_dlp as youtube_dl
import asyncio
from collections import deque

# Настройки для youtube_dl
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

# Настройки для ffmpeg
ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(disnake.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(disnake.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# Очередь треков
playlist = deque()

def setup_music_commands(bot: commands.Bot):
    @bot.slash_command(name='mus_join', description='Включит рекомендованный плейлист Nanson.')
    async def mus_join(inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()

        channel = inter.author.voice.channel
        if not channel:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Вы должны быть в голосовом канале, чтобы использовать эту команду.",
                color=disnake.Color.red()
            )
            await inter.edit_original_message(embed=embed)
            return

        try:
            youtube_url = "https://www.youtube.com/watch?v=ecbWJNADUMs&list=PL08yb2oZ3X90ip5SdXZRWC4XQhnruQhXx"
            vc = await channel.connect()

            player = await YTDLSource.from_url(youtube_url, loop=bot.loop, stream=True)
            vc.play(player, after=lambda e: print(f'Ошибка плеера: {e}') if e else None)

            embed = disnake.Embed(
                title="🎵 Воспроизведение началось",
                description=f"Трек: {player.title}\n\nСсылка на трек: [YouTube]({youtube_url})",
                color=disnake.Color.green()
            )
            embed.set_footer(text=f"Команду выполнил: {inter.author.name}")
            await inter.edit_original_message(embed=embed)

            check_for_empty_channel.start(vc)

        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Произошла ошибка: {str(e)}",
                color=disnake.Color.red()
            )
            await inter.edit_original_message(embed=embed)
            print(f"Ошибка: {str(e)}")

    @bot.slash_command(name='mus_stop', description='Остановить воспроизведение и отключиться от голосового канала.')
    async def mus_stop(inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()

        if inter.guild.voice_client is None:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Бот не подключен к голосовому каналу.",
                color=disnake.Color.red()
            )
            await inter.edit_original_message(embed=embed)
            return

        try:
            vc = inter.guild.voice_client
            if vc.is_playing():
                vc.stop()

            await vc.disconnect()
            playlist.clear()

            embed = disnake.Embed(
                title="🛑 Остановлено",
                description="Воспроизведение остановлено, и бот отключился от голосового канала.",
                color=disnake.Color.red()
            )
            await inter.edit_original_message(embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Произошла ошибка: {str(e)}",
                color=disnake.Color.red()
            )
            await inter.edit_original_message(embed=embed)
            print(f"Ошибка: {str(e)}")

    @bot.slash_command(name='mus_play', description='Поиск и воспроизведение песни с YouTube по запросу.')
    async def mus_play(inter: disnake.ApplicationCommandInteraction, query: str):
        await inter.response.defer()
        try:
            channel = inter.author.voice.channel
            if not channel:
                embed = disnake.Embed(
                    title="❌ Ошибка",
                    description="Вы должны быть в голосовом канале, чтобы использовать эту команду.",
                    color=disnake.Color.red()
                )
                await inter.edit_original_message(embed=embed)
                return

            search_url = f"ytsearch:{query}"
            data = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(search_url, download=False))

            if 'entries' not in data:
                embed = disnake.Embed(
                    title="❌ Ошибка",
                    description="Не удалось найти видео по запросу.",
                    color=disnake.Color.red()
                )
                await inter.edit_original_message(embed=embed)
                return

            entries = data['entries'][:5]
            options = [f"{i+1}. {entry['title']}" for i, entry in enumerate(entries)]
            options_str = "\n".join(options)

            embed = disnake.Embed(
                title="🔍 Результаты поиска",
                description=f"Выберите номер трека для воспроизведения:\n{options_str}",
                color=disnake.Color.blue()
            )
            message = await inter.edit_original_message(embed=embed)

            def check(m):
                return m.author == inter.author and m.channel == inter.channel and m.content.isdigit()

            try:
                msg = await bot.wait_for('message', timeout=60.0, check=check)
                choice = int(msg.content) - 1
                if choice < 0 or choice >= len(entries):
                    raise ValueError("Неверный выбор")

                selected_entry = entries[choice]
                youtube_url = selected_entry['url']

                playlist.append(youtube_url)

                if not inter.guild.voice_client:
                    vc = await channel.connect()
                    await play_next_track(vc)
                else:
                    embed = disnake.Embed(
                        title="🎵 Трек добавлен в плейлист",
                        description=f"Трек: {selected_entry['title']}\n\nСсылка на трек: [YouTube]({youtube_url})",
                        color=disnake.Color.green()
                    )
                    await inter.edit_original_message(embed=embed)

                check_for_empty_channel.start(inter.guild.voice_client)

            except asyncio.TimeoutError:
                embed = disnake.Embed(
                    title="❌ Ошибка",
                    description="Истекло время выбора трека.",
                    color=disnake.Color.red()
                )
                await inter.edit_original_message(embed=embed)
            except Exception as e:
                embed = disnake.Embed(
                    title="❌ Ошибка",
                    description=f"Произошла ошибка: {str(e)}",
                    color=disnake.Color.red()
                )
                await inter.edit_original_message(embed=embed)
                print(f"Ошибка: {str(e)}")

        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Произошла ошибка: {str(e)}",
                color=disnake.Color.red()
            )
            await inter.edit_original_message(embed=embed)
            print(f"Ошибка: {str(e)}")

    @bot.slash_command(name='mus_playlist', description='Показать текущий трек и плейлист.')
    async def mus_playlist(inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()

        if inter.guild.voice_client is None:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Бот не подключен к голосовому каналу.",
                color=disnake.Color.red()
            )
            await inter.edit_original_message(embed=embed)
            return

        try:
            vc = inter.guild.voice_client
            current_track = "Нет воспроизведения" if not vc.is_playing() else vc.source.title
            queue = "\n".join([f"{i+1}. {track}" for i, track in enumerate(playlist)])

            embed = disnake.Embed(
                title="📜 Плейлист",
                description=f"Текущий трек: {current_track}\n\nОчередь:\n{queue if queue else 'Плейлист пуст.'}",
                color=disnake.Color.blue()
            )
            await inter.edit_original_message(embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Произошла ошибка: {str(e)}",
                color=disnake.Color.red()
            )
            await inter.edit_original_message(embed=embed)
            print(f"Ошибка: {str(e)}")

    async def play_next_track(vc):
        if playlist:
            url = playlist.popleft()
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            vc.play(player, after=lambda e: asyncio.create_task(play_next_track(vc)) if playlist else None)

    @tasks.loop(seconds=60)
    async def check_for_empty_channel(vc):
        if len(vc.channel.members) == 1:  # Только бот в канале
            await vc.disconnect()
            check_for_empty_channel.stop()
