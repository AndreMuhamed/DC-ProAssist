import disnake

translations = {
    "ru": {
        "add_socials": "Добавить ссылки на социальные сети.",
        "invalid_vk": "Неверная ссылка на VK.",
        "invalid_telegram": "Неверная ссылка на Telegram.",
        "invalid_instagram": "Неверная ссылка на Instagram.",
        "social_updated": "Социальные сети обновлены! Теперь у вас есть новые функции, которые помогут вам легче делиться вашим профилем в социальных сетях.",
        "no_changes": "Нет изменений для обновления. Но вы всегда можете редактировать и делиться своим профилем в социальных сетях.",
        "profile_created": "Профиль создан.",
        "success_message": "Спасибо, что пользуетесь нашим ботом!"
    },
    "en": {
        "add_socials": "Add links to social networks.",
        "invalid_vk": "Invalid VK link.",
        "invalid_telegram": "Invalid Telegram link.",
        "invalid_instagram": "Invalid Instagram link.",
        "social_updated": "Social media has been updated! Now you have new features that will help you share your profile on social networks more easily.",
        "no_changes": "There are no updates available. However, you can always edit and share your profile on social media.",
        "profile_created": "Profile created.",
        "success_message": "Thank you for using our bot!"
    },
    "uk": {
        "add_socials": "Додати посилання до соціальних мереж.",
        "invalid_vk": "Невірне посилання на VK.",
        "invalid_telegram": "Невірне посилання на Telegram.",
        "invalid_instagram": "Невірне посилання на Instagram.",
        "social_updated": "Соціальні мережі оновлено! Тепер у вас є нові функції, які допоможуть вам легше ділитися своїм профілем у соцмережах.",
        "no_changes": "Немає змін для оновлення. Але ви завжди можете редагувати та ділитися своїм профілем у соцмережах.",
        "profile_created": "Профіль створено.",
        "success_message": "Дякуємо, що користуєтеся нашим ботом!"
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