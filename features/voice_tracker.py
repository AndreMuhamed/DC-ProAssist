import disnake
from disnake.ext import commands
import datetime
import json
import os
import traceback
import re

# Глобальная переменная для хранения времени подключения
join_times = {}

# Функция для загрузки данных о пользователях
def load_user_data():
    if os.path.exists("admin/user_data.json"):
        with open("admin/user_data.json", "r") as file:
            return json.load(file)
    return {}

# Функция для сохранения данных о пользователях
def save_user_data(data):
    # Проверяем, существует ли директория, и создаем ее, если нет
    if not os.path.exists("admin"):
        os.makedirs("admin")
    
    with open("admin/user_data.json", "w") as file:
        json.dump(data, file, indent=4)

import re  # Для работы с регулярными выражениями

# Функция для преобразования строки "45 h, 53 m" в минуты
def convert_time_to_minutes(time_str):
    match = re.match(r"(\d+)\s*h,\s*(\d+)\s*m", time_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        return hours * 60 + minutes
    return 0  # Если формат неправильный, возвращаем 0

# Функция для преобразования минут в строку "45 h, 53 m"
def convert_minutes_to_time(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours} h, {remaining_minutes} m"

# Функция для обновления времени в голосовых каналах и начисления наград
def update_voice_time(user_id, duration):
    user_data = load_user_data()
    
    # Если данных о пользователе нет, создаём запись
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {"voice_online": 0, "rewards": 0}
    
    # Проверяем, является ли "voice_online" строкой и преобразуем её в минуты
    if isinstance(user_data[str(user_id)]["voice_online"], str):
        user_data[str(user_id)]["voice_online"] = convert_time_to_minutes(user_data[str(user_id)]["voice_online"])
    
    # Преобразуем "rewards" в число, если это строка
    user_data[str(user_id)]["rewards"] = int(user_data[str(user_id)]["rewards"])
    
    # Обновляем время и вознаграждение
    user_data[str(user_id)]["voice_online"] += duration
    user_data[str(user_id)]["rewards"] += (duration // 60) * 35  # 8 монет за каждый час
    
    # Преобразуем обратно минуты в формат "h, m"
    user_data[str(user_id)]["voice_online"] = convert_minutes_to_time(user_data[str(user_id)]["voice_online"])
    
    # Сохраняем обновлённые данные
    save_user_data(user_data)

# Основная функция для отслеживания голосовой активности
def setup_voice_tracker(bot):
    @bot.event
    async def on_voice_state_update(member, before, after):
        try:
            user_id = member.id
            
            # Пользователь подключился к голосовому каналу
            if before.channel is None and after.channel is not None:
                join_times[user_id] = datetime.datetime.now()

            # Пользователь отключился от голосового канала
            elif before.channel is not None and after.channel is None:
                if user_id in join_times:
                    join_time = join_times.pop(user_id)
                    time_spent = datetime.datetime.now() - join_time
                    duration = int(time_spent.total_seconds() // 60)  # Время в минутах
                    update_voice_time(user_id, duration)
        
        except Exception as e:
            # Логируем ошибку
            print(f"An unexpected error occurred in on_voice_state_update: {e}")
            traceback.print_exc()  # Печатаем полный стек ошибки















