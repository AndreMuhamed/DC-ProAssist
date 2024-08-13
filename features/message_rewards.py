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

        if user_id not in data:
            data[user_id] = {"rewards": 0}
        
        data[user_id]["rewards"] += 150
        self.save_data(data)

        print(f"Added 5 coins to user {user_id}. Total: {data[user_id]['rewards']}")

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
