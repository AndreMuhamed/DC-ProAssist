import disnake

translations = {
    "ru": {
        "welcome_title": "Добро пожаловать на сервер!",
        "welcome_message": "Привет, {member}! Ты находишься на одном из проектов **Андрея Мухамеда**.",
        "recommendation": "Рекомендуем подписаться на его другие проекты на YouTube, нажав на кнопки ниже под этим сообщением. **Заранее благодарим!**",
        "footer_text": "Спасибо за вашу будущую активность!",
    },
    "uk": {
        "welcome_title": "Ласкаво просимо на сервер!",
        "welcome_message": "Привіт, {member}! Ти знаходишся на одному з проектів **Андрія Мухамеда**.",
        "recommendation": "Рекомендуємо підписатися на його інші проекти на YouTube, натиснувши на кнопки нижче під цим повідомленням. **Заздалегідь дякуємо!**",
        "footer_text": "Дякуємо за вашу майбутню активність!",
    },
    "en": {
        "welcome_title": "Welcome to the server!",
        "welcome_message": "Hi, {member}! You are on one of **Andrey Mukhamed's** projects.",
        "recommendation": "We recommend subscribing to his other projects on YouTube by clicking the buttons below this message. **Thank you in advance!**",
        "footer_text": "Thank you for your future activity!",
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