import disnake


translations = {
    "en": {
        "listen_podcast": "<:icons13:1274836249810698250> Listen to our mini-podcast!",
        "interesting_today": "Today, the team of **Andrey Muhameda** has prepared an incredible podcast for you, filled with **fascinating** topics and interesting conversations.",
        "footer_text": "Dive into a world of knowledge and inspiration!",
        "error_occurred": "An error occurred while processing the command.",
        "must_be_in_voice": "You must be in a voice channel to play music.",
        "stream_error": "Failed to get the stream for playback."
    },
    "ru": {
        "listen_podcast": "<:icons13:1274836249810698250> Слушай наш мини-подкаст!",
        "interesting_today": "Сегодня команда **Андрея Мухамеда** подготовила для вас невероятный подкаст, наполненный **увлекательными** темами и интересными беседами.",
        "footer_text": "Погружайтесь в мир знаний и вдохновения!",
        "error_occurred": "Произошла ошибка при обработке команды.",
        "must_be_in_voice": "Вы должны находиться в голосовом канале, чтобы воспроизвести музыку.",
        "stream_error": "Не удалось получить поток для воспроизведения."
    },
    "uk": {
        "listen_podcast": "<:icons13:1274836249810698250> Слухай наш міні-подкаст!",
        "interesting_today": "Сьогодні команда **Андрея Мухамеда** підготувала для вас неймовірний подкаст, наповнений **цікавими** темами та захоплюючими бесідами.",
        "footer_text": "Пориньте у світ знань та натхнення!",
        "error_occurred": "Сталася помилка під час обробки команди.",
        "must_be_in_voice": "Ви повинні бути в голосовому каналі, щоб відтворювати музику.",
        "stream_error": "Не вдалося отримати потік для відтворення."
    }
}

def get_user_language(inter: disnake.ApplicationCommandInteraction) -> str:
    # Преобразуем locale в строку
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