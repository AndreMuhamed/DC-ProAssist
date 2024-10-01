import disnake
from disnake.ext import commands
from datetime import datetime
import json
import re
import os

# Глобальный словарь для хранения времени подключения
join_times = {}

def load_data():
    user_data_path = 'admin/user_data.json'
    if os.path.exists(user_data_path):
        try:
            with open(user_data_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    else:
        return {}

def save_data(data):
    user_data_path = 'admin/user_data.json'
    try:
        with open(user_data_path, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Ошибка записи данных пользователя: {e}")

def update_voice_online(user_id, duration):
    data = load_data()
    
    # Инициализация данных пользователя, если не существует
    if user_id not in data:
        data[user_id] = {
            "status": None,
            "rewards": "0",
            "voice_online": "0 h, 0 m",
            "last_claim": None,
            "profile_created": datetime.utcnow().strftime("%d.%m.%Y")
        }

    user_data = data[user_id]
    
    # Инициализация rewards если не существует
    if 'rewards' not in user_data:
        user_data['rewards'] = 0

    # Обновление времени в голосовых каналах
    current_online_time = user_data.get("voice_online", "0 ч, 0 м")
    # Обработка строки времени
    try:
        hours, minutes = map(int, re.findall(r'\d+', current_online_time))
    except ValueError:
        hours, minutes = 0, 0

    total_minutes = hours * 60 + minutes + duration
    new_hours, new_minutes = divmod(total_minutes, 60)
    user_data["voice_online"] = f"{new_hours} ч, {new_minutes} м"
    
    # Вознаграждение за каждый час
    rewards_gained = (duration // 60) * 8  # 48 монет за каждый час
    user_data["rewards"] += rewards_gained

    data[user_id] = user_data
    save_data(data)
    
    return rewards_gained  # Возвращаем количество полученных наград

def setup_voice_tracker(bot: commands.Bot):
    @bot.event
    async def on_voice_state_update(member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        user_id = str(member.id)
        if before.channel is None and after.channel is not None:
            # Пользователь подключился к голосовому каналу
            join_times[user_id] = datetime.utcnow()
        elif before.channel is not None and after.channel is None:
            # Пользователь отключился от голосового канала
            if user_id in join_times:
                duration = (datetime.utcnow() - join_times[user_id]).seconds // 60
                del join_times[user_id]  # Удаляем запись времени подключения
                update_voice_online(user_id, duration)










