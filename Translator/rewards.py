import disnake 

translations = {
    "ru": {
        "view_reward": "Получить награду в виде монет.",
        "reward_received": "Вознаграждение получено — {name}",
        "reward_message": "Вы получили вознаграждение в сумме **{amount}** монет.\nТеперь у вас в профиле **{total}** монет.",
        "reward_already_claimed": "Вознаграждение уже получено — {name}",
        "already_claimed_message": "Вы **уже** получили **вознаграждение!**\nВы можете **получить** следующую через **{hours}** ч **{minutes}** мин.",
        "thank_you": "Спасибо за вашу активность!",
        "buy_coins": "Купить монеты",
        "purchase_title": "Покупка монет в Online Shop!",
        "purchase_message": "Спасибо за интерес к покупке монет! Для завершения покупки, пожалуйста, свяжитесь с продавцом.",
        "seller_link": "Ссылка на продавцов:",
    },
    "uk": {
        "view_reward": "Отримати нагороду у вигляді монет.",
        "reward_received": "Нагорода отримана — {name}",
        "reward_message": "Ви отримали нагороду в сумі **{amount}** монет.\nТепер у вас у профілі **{total}** монет.",
        "reward_already_claimed": "Нагорода вже отримана — {name}",
        "already_claimed_message": "Ви **вже** отримали **нагороду!**\nВи можете **отримати** наступну через **{hours}** год **{minutes}** хв.",
        "thank_you": "Дякуємо за вашу активність!",
        "buy_coins": "Купити монети",
        "purchase_title": "Купівля монет в Online Shop!",
        "purchase_message": "Дякуємо за інтерес до купівлі монет! Для завершення покупки, будь ласка, зв'яжіться з продавцем.",
        "seller_link": "Посилання на продавців:",
    },
    "en": {
        "view_reward": "Get rewarded with coins.",
        "reward_received": "Reward received — {name}",
        "reward_message": "You received a reward of **{amount}** coins.\nNow you have **{total}** coins in your profile.",
        "reward_already_claimed": "Reward already claimed — {name}",
        "already_claimed_message": "You have **already** claimed your **reward!**\nYou can **claim** the next one in **{hours}** h **{minutes}** m.",
        "thank_you": "Thank you for your activity!",
        "buy_coins": "Buy coins",
        "purchase_title": "Buying coins in Online Shop!",
        "purchase_message": "Thank you for your interest in buying coins! To complete the purchase, please contact the seller.",
        "seller_link": "Link to sellers:",
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