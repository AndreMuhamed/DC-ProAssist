import disnake       
from disnake.ext import commands
import asyncio
import os
import random  # Импортируем модуль random
from Translator.playlist import translations, get_user_language

MUSIC_FOLDER = 'assets/music/'  # Путь к папке с файлами OPUS

class Playlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Метод для отправки сообщений об ошибках
    async def send_error_embed(self, ctx, message):
        lang = get_user_language(ctx)
        embed = disnake.Embed(
            title=translations[lang]["error_title"],
            description=message
        )
        # Устанавливаем аватар пользователя
        embed.set_thumbnail(url=ctx.author.display_avatar.url if ctx.author.display_avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)

    # Подключение к голосовому каналу
    async def connect_to_channel(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            return voice
        else:
            await self.send_error_embed(ctx, translations[get_user_language(ctx)]["must_be_in_voice"])
            return None

    # Проигрывание музыки в формате OPUS
    async def play_opus_music(self, voice_client, ctx, duration):
        files = os.listdir(MUSIC_FOLDER)
        opus_files = [f for f in files if f.endswith('.opus')]
        
        if not opus_files:
            await self.send_error_embed(ctx, translations[get_user_language(ctx)]["no_opus_files"])
            return

        total_time_played = 0

        while total_time_played < duration * 60:  # Время в секундах
            # Проверяем, есть ли участники в голосовом канале
            if len(voice_client.channel.members) == 0:
                await voice_client.disconnect()  # Отключаемся, если никого нет
                return  # Выходим из функции, не отправляя сообщение

            # Проигрываем случайный файл OPUS
            opus_file = random.choice(opus_files)  # Выбираем случайный файл
            voice_client.play(disnake.FFmpegPCMAudio(f"{MUSIC_FOLDER}/{opus_file}"))

            # Ждем, пока трек закончится или пока никого нет в канале
            while voice_client.is_playing():
                # Проверяем, есть ли участники в голосовом канале
                if len(voice_client.channel.members) == 0:
                    await voice_client.disconnect()  # Отключаемся, если никого нет
                    return  # Выходим из функции, не отправляя сообщение
                await asyncio.sleep(1)  # Ждем 1 секунду

            # После завершения трека увеличиваем общее время проигрывания
            total_time_played += 180  # Предполагаем, что каждая песня длится 3 минуты

            # Если общее время проигрывания больше или равно желаемому, выходим из цикла
            if total_time_played >= duration * 60:
                break

    @commands.slash_command(name="play_playlist", description='Playing a playlist from Nanson.')
    async def play_playlist(self, inter: disnake.ApplicationCommandInteraction, minutes: int):
        """Играет музыку из папки в течение заданного времени"""
        await inter.response.defer()

        # Определение языка пользователя
        user_lang = get_user_language(inter)

        # Подключение к голосовому каналу
        voice = await self.connect_to_channel(inter)
        if voice is None:
            return

        # Получение названия голосового канала
        voice_channel_name = inter.author.voice.channel.name if inter.author.voice else "Неизвестный канал"

        # Создание и отправка embed-сообщения
        embed = disnake.Embed(
            title=translations[user_lang]["playing_playlist"],
            description=translations[user_lang]["playlist_description"].format(
                channel_name=inter.guild.name, 
                voice_channel=voice_channel_name, 
                minutes=minutes
            ),
        )
        embed.set_footer(text=translations[user_lang]["footer_text"])  # Текст подвала
        embed.set_image(url=translations[user_lang]["embed_thumbnail_url"])  # Замените на URL изображения

        await inter.edit_original_message(embed=embed)

        # Проигрывание музыки
        await self.play_opus_music(voice, inter, minutes)

        # Отключение после завершения
        await voice.disconnect()

# Регистрация кода
def setup(bot):
    bot.add_cog(Playlist(bot))




