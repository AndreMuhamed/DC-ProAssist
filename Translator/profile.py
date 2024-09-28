import disnake

translations = {
    "ru": {
        "view_profile": "Просмотреть профиль пользователя.",
        "add_socials": "Добавить ссылки на социальные сети.",
        "status": "Статус",
        "no_status": "Нет статуса",
        "coins": "Монеты",
        "no_voice_time": "0 ч, 0 м",
        "voice_online": "Голосовой онлайн",
        "profile_created": "Профиль создан",
        "not_provided": "Не указано",
        "profile_title": "Профиль — {user}",
        "buy_coins": "Купить монеты",
        "invalid_vk": "Неверная ссылка на VK.",
        "invalid_telegram": "Неверная ссылка на Telegram.",
        "invalid_instagram": "Неверная ссылка на Instagram.",
        "social_updated": "Социальные сети обновлены.",
        "seller_link_title": "Ссылка на продавцов:",
        "buy_coins_title": "Покупка монет в Online Shop!",
        "buy_coins_description": "Спасибо за интерес к покупке монет! Для завершения покупки, пожалуйста, свяжитесь с продавцом.",
    },
    "en": {
        "view_profile": "View user profile.",
        "add_socials": "Add links to social networks.",
        "status": "Status",
        "no_status": "No status",
        "coins": "Coins",
        "no_voice_time": "0 h, 0 m",
        "voice_online": "Voice online",
        "profile_created": "Profile created",
        "not_provided": "Not provided",
        "profile_title": "Profile — {user}",
        "buy_coins": "Buy coins",
        "invalid_vk": "Invalid VK link.",
        "invalid_telegram": "Invalid Telegram link.",
        "invalid_instagram": "Invalid Instagram link.",
        "social_updated": "Social media updated.",
        "seller_link_title": "Seller link:",
        "buy_coins_title": "Buying coins in Online Shop!",
        "buy_coins_description": "Thank you for your interest in buying coins! To complete your purchase, please contact the seller.",
    },
    "uk": {
        "view_profile": "Переглянути профіль користувача.",
        "add_socials": "Додати посилання до соціальних мереж.",
        "status": "Статус",
        "no_status": "Немає статусу",
        "coins": "Монети",
        "no_voice_time": "0 год, 0 хв",
        "voice_online": "Голосовий онлайн",
        "profile_created": "Профіль створено",
        "not_provided": "Не вказано",
        "profile_title": "Профіль — {user}",
        "buy_coins": "Купити монети",
        "invalid_vk": "Невірне посилання на VK.",
        "invalid_telegram": "Невірне посилання на Telegram.",
        "invalid_instagram": "Невірне посилання на Instagram.",
        "social_updated": "Соціальні мережі оновлено.",
        "seller_link_title": "Посилання на продавців:",
        "buy_coins_title": "Купівля монет в Online Shop!",
        "buy_coins_description": "Дякуємо за інтерес до купівлі монет! Щоб завершити покупку, будь ласка, зв'яжіться з продавцем.",
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





