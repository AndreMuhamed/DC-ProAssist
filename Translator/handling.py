import disnake

translations = {
    'ru': {
        'title': "<:Stickerus5:1269746098809864232> Команда не найдена!",
        'description': "Извините, команда `{command}` **не распознана**.",
        'hint': "Начните сначала, но это не точно."
    },
    'en': {
        'title': "<:Stickerus5:1269746098809864232> Command not found!",
        'description': "Sorry, the command `{command}` **was not recognized**.",
        'hint': "Start all over, but it's not accurate."
    },
    'uk': {
        'title': "<:Stickerus5:1269746098809864232> Команда не знайдена!",
        'description': "Вибачте, команда `{command}` **не розпізнана**.",
        'hint': "Почніть спочатку, але це не точно."
    }
}

def get_user_language(ctx: disnake.ApplicationCommandInteraction) -> str:
    # Проверяем, если это обычное сообщение или взаимодействие
    if isinstance(ctx, disnake.ApplicationCommandInteraction):
        user_locale = str(ctx.locale)
    else:
        # Для текстовых команд (message context)
        user_locale = str(ctx.guild.preferred_locale) if ctx.guild else 'ru'

    print(f"User locale: {user_locale}")  # Для отладки

    if user_locale.startswith("ru"):
        return "ru"
    elif user_locale.startswith("uk"):
        return "uk"
    elif user_locale.startswith("en"):
        return "en"
    else:
        return "ru"  # Русский по умолчанию для всех других языков
