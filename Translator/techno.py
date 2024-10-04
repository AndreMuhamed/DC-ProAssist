import disnake

translations = {
    "ru": {
        "bot_confused_title": "<:icons6:1274836186984218644> Бот запутался!",
        "bot_confused_description": "Ой, кажется **что-то** пошло не так. Мы уже пытаемся разобраться в проблеме! **Но это не точно**",
        "test_command_description": "Не жми сюда, если не хочешь увидеть смерть!"
    },
    "en": {
        "bot_confused_title": "<:icons6:1274836186984218644> The bot is confused!",
        "bot_confused_description": "Oops, **something** went wrong. We're already trying to figure it out! **But that's not certain**",
        "test_command_description": "Don't press here if you don't want to see death!"
    },
    "uk": {
        "bot_confused_title": "<:icons6:1274836186984218644> Бот заплутався!",
        "bot_confused_description": "Ой, здається, **щось** пішло не так. Ми вже намагаємось розібратися в проблемі! **Але це не точно**",
        "test_command_description": "Не натискайте сюди, якщо не хочете побачити смерть!"
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



