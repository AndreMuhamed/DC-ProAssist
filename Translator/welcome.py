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

def get_user_language(member: disnake.Member) -> str:
    # Получаем предпочтительный язык
    user_language = member.locale or member.preferred_locale
    if user_language:
        return user_language.split('-')[0]  # Возвращаем только код языка
    return 'ru'  # Русский по умолчанию