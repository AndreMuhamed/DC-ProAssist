import disnake


translations = {
    "en": {
        "error_title": "<:icons65:1274836965111496714> Playlist Error!",
        "must_be_in_voice": "```You must be in a voice channel to play the playlist from Nanson.```",
        "no_opus_files": "There are no OPUS files in the folder.",
        "playing_playlist": "<:icons38:1274836476642852985> Listening to the playlist from Nanson!",
        "playlist_description": "A wonderful **playback** tailored just **for you** will begin shortly, so enjoy the harmony of songs from different genres!\n\nMusic is playing on the server: **{channel_name}**\nIn an awesome voice channel: **{voice_channel}**\nThe playlist will play for: **{minutes}** minutes.",
        "footer_text": "Relax and enjoy life!",
        "embed_thumbnail_url": "https://cdn.discordapp.com/attachments/1089651879836913817/1292075574008741950/2dbce13d32fc38c2.jpg"
    },
    "ru": {
        "error_title": "<:icons65:1274836965111496714> Ошибка плейлиста!",
        "must_be_in_voice": "```Вы должны быть в голосовом канале, чтобы воспроизводить плейлист от Nanson.```",
        "no_opus_files": "В папке нет файлов формата OPUS.",
        "playing_playlist": "<:icons38:1274836476642852985> Слушаем плейлист от Nanson!",
        "playlist_description": "Сейчас начнется замечательное **проигрывание**, подобранное специально **для вас**, так что наслаждайтесь гармонией песен разных жанров!\n\nМузыка играет на сервере: **{channel_name}**\nВ крутом голосовом канале: **{voice_channel}**\nПлейлист будет играть: **{minutes}** минут.",
        "footer_text": "Отдыхай и наслаждайся жизнью!",
        "embed_thumbnail_url": "https://cdn.discordapp.com/attachments/1089651879836913817/1292075574008741950/2dbce13d32fc38c2.jpg"
    },
    "uk": {
        "error_title": "<:icons65:1274836965111496714> Помилка плейлиста!",
        "must_be_in_voice": "```Ви повинні бути в голосовому каналі, щоб відтворювати плейлист від Nanson.```",
        "no_opus_files": "У папці немає файлів формату OPUS.",
        "playing_playlist": "<:icons38:1274836476642852985> Слухаємо плейлист від Nanson!",
        "playlist_description": "Зараз розпочнеться чудове **відтворення**, підібране спеціально **для вас**, так що насолоджуйтесь гармонією пісень різних жанрів!\n\nМузика грає на сервері: **{channel_name}**\nУ класному голосовому каналі: **{voice_channel}**\nПлейлист буде грати: **{minutes}** хвилин.",
        "footer_text": "Відпочивай і насолоджуйся життям!",
        "embed_thumbnail_url": "https://cdn.discordapp.com/attachments/1089651879836913817/1292075574008741950/2dbce13d32fc38c2.jpg"
    }
}

def get_user_language(inter: disnake.ApplicationCommandInteraction) -> str:
    """Определяет язык пользователя на основе его локали."""
    user_locale = str(inter.locale)
    print(f"User locale: {user_locale}")  # Для отладки

    if user_locale.startswith("ru"):
        return "ru"
    elif user_locale.startswith("uk"):
        return "uk"
    elif user_locale.startswith("en"):
        return "en"
    else:
        return "ru"  # Русский по умолчанию для всех других языков