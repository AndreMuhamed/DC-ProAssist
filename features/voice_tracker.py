import disnake
from disnake.ext import commands
from datetime import datetime
import json
import re
import os

# Глобальный словарь для хранения времени подключения
join_times = {}

def load_user_data():
    user_data_file = 'admin/user_data.json'
    if os.path.exists(user_data_file):
        try:
            with open(user_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка загрузки данных пользователя: {e}")
            return {}
    return {}

def save_user_data(data):
    user_data_file = 'admin/user_data.json'
    try:
        with open(user_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Ошибка записи данных пользователя: {e}")

def update_voice_time(user_id, duration):
    data = load_user_data()
    
    if user_id not in data:
        data[user_id] = {
            "status": None,
            "rewards": 0,
            "voice_online": "0 h, 0 m",
            "last_claim": None,
            "profile_created": datetime.utcnow().strftime("%d.%m.%Y")
        }

    user_data = data[user_id]
    
    current_online_time = user_data.get("voice_online", "0 h, 0 m")
    
    # Разбор текущего времени
    try:
        hours, minutes = map(int, re.findall(r'\d+', current_online_time))
    except ValueError as e:
        print(f"Ошибка разбора времени: {e}")
        hours, minutes = 0, 0

    # Проверка на корректность типа duration
    if isinstance(duration, int):
        total_minutes = hours * 60 + minutes + duration
    else:
        print(f"Ошибка: Длительность должна быть целым числом, получено: {type(duration)}")
        total_minutes = hours * 60 + minutes  # Без добавления длительности

    new_hours, new_minutes = divmod(total_minutes, 60)
    
    # Форматирование строки с новым временем
    user_data["voice_online"] = f"{new_hours} h, {new_minutes} m"
    
    # Расчет вознаграждений
    rewards_gained = (duration // 60) * 8  # 8 монет за каждый час
    user_data["rewards"] += rewards_gained

    data[user_id] = user_data
    save_user_data(data)
    
    return rewards_gained

def setup_voice_tracker(bot: commands.Bot):
    @bot.event
    async def on_voice_state_update(member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        user_id = str(member.id)
        try:
            if before.channel is None and after.channel is not None:
                join_times[user_id] = datetime.utcnow()
            elif before.channel is not None and after.channel is None:
                if user_id in join_times:
                    duration = (datetime.utcnow() - join_times[user_id]).seconds // 60
                    del join_times[user_id]
                    
                    # Проверка на корректность типа duration
                    if duration < 0:
                        print(f"Ошибка: Длительность не может быть отрицательной: {duration}")
                    else:
                        print(f"Пользователь {member.display_name} отключился. Длительность: {duration} минут.")
                    
                    rewards = update_voice_time(user_id, duration)
                    print(f"Пользователь {member.display_name} заработал {rewards} наград.")
        except Exception as e:
            print(f"Ошибка в on_voice_state_update: {e}")












