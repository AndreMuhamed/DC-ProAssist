import disnake
from admin.data_handler import update_last_sent, save_data

async def send_auto_reply(message: disnake.Message, data, user_id):
    """Отправляет сообщение с гифкой в ответ на сообщение пользователя и обновляет дату последнего сообщения."""
    channel = message.channel
    if isinstance(channel, disnake.DMChannel) and not message.author.bot:
        embed = disnake.Embed(
            title="<:Stickerus13:1269746163452608666> Оповещение!",
            description=(
                "Бот работает **24/7** над проектами **Андрея Мухамеда**.\n"
                "И не имеет возможности **отвечать** на твои крутые сообщения.\n\n"
                "Посетите [этот сайт](https://andremuhamed.nexcord.pro/) для получения дополнительной информации!"
            ),
        )
        # Убедитесь, что путь к файлу верный
        with open('assets/working_24_7.gif', 'rb') as f:
            file = disnake.File(f, filename='response.gif')
            embed.set_image(url='attachment://response.gif')

        await channel.send(embed=embed, file=file)

        # Обновляем дату последнего сообщения
        update_last_sent(data, user_id)
        save_data(data)




