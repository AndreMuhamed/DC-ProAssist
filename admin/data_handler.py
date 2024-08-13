from datetime import datetime
import json
import os

data_file = 'admin/user_data.json'

def load_data():
    """Загружает данные профилей из файла."""
    if not os.path.exists(data_file):
        return {"last_sent": {}, "channel_ids": []}  # Если файла нет, возвращаем структуру по умолчанию
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Ошибка чтения данных из файла.")
        return {"last_sent": {}, "channel_ids": []}

def save_data(data):
    """Сохраняет данные профилей в файл."""
    try:
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)  # Сортируем ключи для удобства
    except IOError as e:
        print(f"Ошибка записи данных: {e}")

def ensure_user_profile(data, user_id):
    """Проверяет, существует ли профиль пользователя, и создает его при необходимости."""
    if user_id not in data:
        data[user_id] = {
            "status": "Нет статуса",
            "rewards": 0,
            "voice_online": "0 ч, 0 м",
            "vk": "Не указано",
            "telegram": "Не указано",
            "instagram": "Не указано",
            "last_claim": None,
            "profile_created": datetime.utcnow().strftime("%d.%m.%Y"),
            "last_sent": datetime.utcnow().isoformat()  # Устанавливаем дату последнего сообщения
        }
        save_data(data)

def update_last_sent(data, user_id):
    """Обновляет поле last_sent для указанного пользователя."""
    if user_id in data:
        data[user_id]['last_sent'] = datetime.utcnow().isoformat()
        save_data(data)










