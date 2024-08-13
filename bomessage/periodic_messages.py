import disnake
import asyncio
import json
from datetime import datetime, timedelta

data_file = 'admin/user_data.json'

# Чтение данных из файла
def load_data():
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_sent": {}, "user_ids": []}

# Запись данных в файл
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

# Обновление времени последней отправки
def update_last_sent(data, user_id):
    data["last_sent"][user_id] = datetime.utcnow().isoformat()
    save_data(data)

# Периодическая задача отправки сообщений
async def send_periodic_reminders(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        data = load_data()
        last_sent = data.get("last_sent", {})
        now = datetime.utcnow()
        two_months_ago = now - timedelta(days=60)

        for user_id in data.get("user_ids", []):
            last_sent_time = datetime.fromisoformat(last_sent.get(user_id, '1970-01-01T00:00:00'))
            if last_sent_time < two_months_ago:
                user = bot.get_user(int(user_id))
                if user:
                    embed = disnake.Embed(
                        title="<:Stickerus2:1269746037577351208> Периодическое обновление!",
                        description="Мы рады сообщить вам, что у **Андрея Мухамеда** есть Telegram бот! Не упустите шанс узнать о новых проектах и событиях!",
                    )
                    embed.add_field(name="Telegram бот:", value="https://t.me/ProManagerss_bot", inline=False)
                    try:
                        await user.send(embed=embed)
                        update_last_sent(data, user_id)
                        print(f"Periodic DM sent to {user_id}")
                    except disnake.Forbidden:
                        print(f"Не удалось отправить сообщение пользователю {user_id}")
                    except Exception as e:
                        print(f"Произошла ошибка при отправке сообщения пользователю {user_id}: {str(e)}")

        await asyncio.sleep(60 * 60 * 24)  # Проверка раз в день

# Функция для настройки периодических задач
def setup_periodic_tasks(bot):
    bot.loop.create_task(send_periodic_reminders(bot))
