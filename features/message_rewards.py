import disnake
from disnake.ext import commands
import json

class MessageRewards(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        data = self.load_data()

        # Проверяем, если пользователь еще не получил награду за первое сообщение
        if user_id not in data or "rewarded" not in data[user_id]:
            # Обновляем данные пользователя
            if user_id not in data:
                data[user_id] = {"rewards": 0}
                
            data[user_id]["rewards"] += 1450
            data[user_id]["rewarded"] = True
            self.save_data(data)

            # Отправляем сообщение в личку
            try:
                embed = disnake.Embed(
                    title="Поздравления о награде!",
                    description=f"Вы получили **награду** за ваше первое сообщение на сервере **Андрея Мухамеда**!",
                ).add_field(
                    name="> Награда:", value="```1450 монет```", inline=False
                ).set_footer(
                    text="Спасибо, что присоединились к нам!"
                ).set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png"  # Замените на URL аватара вашего магазина
                )

                await message.author.send(embed=embed)
            except disnake.Forbidden:
                print(f"Не удалось отправить личное сообщение пользователю {message.author.id}")

        await self.bot.process_commands(message)

    def load_data(self):
        try:
            with open('admin/user_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("File not found. Returning empty data.")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return {}

    def save_data(self, data):
        try:
            with open('admin/user_data.json', 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"File IO Error: {e}")

def setup(bot: commands.Bot):
    bot.add_cog(MessageRewards(bot))


