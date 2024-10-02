import disnake
from disnake.ext import commands, tasks
import json
from datetime import datetime, timedelta, timezone
from supecomma.config import ROLES

def setup_shop_status(bot: commands.Bot):
    @bot.slash_command(name='shop_status', description='Показать магазин статусов.')
    async def shop_status(inter: disnake.ApplicationCommandInteraction):
        await send_shop_page(inter, page=1, new_message=True)

    async def send_shop_page(inter: disnake.ApplicationCommandInteraction, page: int, new_message: bool = False):
        prices = {
            "COMMUNITY DONATER": 800, "MODERATOR": 1200, "THE VIOLATOR": 100, "Большой Пук": 3000, "Король Бури": 350,
            "Чародей Света": 300, "Властелин Теней": 250, "Алхимик Бессмертия": 200, "Страж Галактики": 150,
            "Повелитель Звезд": 100, "Малой писюн": 250, "Волшебник Стихий": 50, "Титан Природы": 400, "Мудрец Безмолвия": 350,
            "Архитектор Снов": 300, "Хранитель Древних Тайн": 250, "Путешественник Времен": 200, "Покоритель Глубин": 150,
            "Маг Восхода": 100, "Создатель Заклинаний": 50, "Заклинатель Туманов": 400, "Царь Ветров": 350,
            "Повелитель Океанов": 300, "Ковбой Виртуальности": 250, "Мастер Порталов": 200, "Властелин Облаков": 150,
            "Колдун Драконов": 100, "Гуру Мистицизма": 400
        }

        data = load_data()
        statuses = list(prices.items())
        items_per_page = 5
        total_pages = (len(statuses) + items_per_page - 1) // items_per_page
        page = max(1, min(page, total_pages))
        start = (page - 1) * items_per_page
        end = start + items_per_page

        embed = disnake.Embed(title="Магазин крутых статусов в профиле!", description="Выберите статус, нажмите на кнопку с номером чтобы купить его.")
        for idx, (status, price) in enumerate(statuses[start:end], start=start + 1):
            purchase_count = data.get('status_purchases', {}).get(status, 0)
            embed.add_field(name=f"> Номер покупки {idx}:  @{status}", value=f"```Стоит {price} монет\nКуплено у бота раз: {purchase_count}```", inline=False)

        embed.set_footer(text=f"Страница {page} из {total_pages}")

        # Разделим кнопки на несколько рядов, чтобы избежать превышения лимита
        action_rows = []
        components = [
            disnake.ui.Button(label=str(idx), style=disnake.ButtonStyle.primary, custom_id=f"buy_{statuses[start + i][0]}")
            for i, idx in enumerate(range(start + 1, end + 1))
        ]
        components.append(disnake.ui.Button(label="Индивидуальный статус", style=disnake.ButtonStyle.success, custom_id="buy_individual_status"))

        # Добавляем компоненты в ряды
        for i in range(0, len(components), 5):
            action_rows.append(disnake.ui.ActionRow(*components[i:i+5]))

        navigation = disnake.ui.ActionRow(
            disnake.ui.Button(label="⏮️", style=disnake.ButtonStyle.secondary, custom_id=f"first_{page}", disabled=page == 1),
            disnake.ui.Button(label="◀️", style=disnake.ButtonStyle.secondary, custom_id=f"prev_{page}", disabled=page == 1),
            disnake.ui.Button(label="▶️", style=disnake.ButtonStyle.secondary, custom_id=f"next_{page}", disabled=page == total_pages),
            disnake.ui.Button(label="⏭️", style=disnake.ButtonStyle.secondary, custom_id=f"last_{page}", disabled=page == total_pages)
        )
        action_rows.append(navigation)

        if new_message:
            await inter.send(embed=embed, components=action_rows)
        else:
            await inter.edit_original_message(embed=embed, components=action_rows)

    @bot.event
    async def on_interaction(inter: disnake.Interaction):
        if isinstance(inter, disnake.MessageInteraction):
            custom_id = inter.data.custom_id
            if custom_id.startswith("buy_"):
                status = custom_id[4:]
                await buy_status(inter, status)
            elif custom_id.startswith("prev_") or custom_id.startswith("next_"):
                page = int(custom_id.split('_')[1])
                new_page = page - 1 if custom_id.startswith("prev_") else page + 1
                await inter.response.defer()
                await send_shop_page(inter, new_page, new_message=False)
            elif custom_id.startswith("first_") or custom_id.startswith("last_"):
                page = int(custom_id.split('_')[1])
                total_pages = (len(load_data()) + 5 - 1) // 5  # Обновляем total_pages перед переходом
                new_page = 1 if custom_id.startswith("first_") else total_pages
                await inter.response.defer()
                await send_shop_page(inter, new_page, new_message=False)
            elif custom_id == "buy_individual_status":
                print("Кнопка 'Индивидуальный статус' нажата")  # Отладочное сообщение
                await handle_individual_status_request(inter)

    async def handle_individual_status_request(inter: disnake.MessageInteraction):
        seller_avatar_url = "https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png"
        
        embed = disnake.Embed(
            title="Покупка статуса в Online Shop!",
            description="Спасибо за интерес к покупке статуса! Для завершения покупки, пожалуйста, свяжитесь с продавцом.",
        )
        embed.add_field(
            name="Ссылка на продавцов:",
            value="<@768782555171782667> или <@787093771115692062>"
        )
        embed.set_thumbnail(url=seller_avatar_url)
        
        await inter.send(embed=embed, ephemeral=True)

    async def buy_status(inter: disnake.MessageInteraction, status: str):
        prices = {
            "COMMUNITY DONATER": 800, "MODERATOR": 1200, "THE VIOLATOR": 100, "Большой Пук": 3000, "Король Бури": 350,
            "Чародей Света": 300, "Властелин Теней": 250, "Алхимик Бессмертия": 200, "Страж Галактики": 150,
            "Повелитель Звезд": 100, "Малой писюн": 250, "Волшебник Стихий": 50, "Титан Природы": 400, "Мудрец Безмолвия": 350,
            "Архитектор Снов": 300, "Хранитель Древних Тайн": 250, "Путешественник Времен": 200, "Покоритель Глубин": 150,
            "Маг Восхода": 100, "Создатель Заклинаний": 50, "Заклинатель Туманов": 400, "Царь Ветров": 350,
            "Повелитель Океанов": 300, "Ковбой Виртуальности": 250, "Мастер Порталов": 200, "Властелин Облаков": 150,
            "Колдун Драконов": 100, "Гуру Мистицизма": 400
        }
        roles = ROLES

        if status not in prices and status != "Индивидуальный статус":
            await inter.response.send_message("Такого статуса не существует.", ephemeral=True)
            return

        user_id = str(inter.author.id)
        data = load_data()
        user_data = data.get(user_id, {"rewards": 0, "status": None})

        if status != "Индивидуальный статус":
            if user_data['rewards'] < prices[status]:
                await inter.response.send_message("У вас недостаточно монет для покупки этого статуса.", ephemeral=True)
                return

            old_status = user_data.get('status', None)
            if old_status:
                old_role_ids = roles.get(old_status, [])
                for guild in bot.guilds:
                    for old_role_id in old_role_ids:
                        old_role = guild.get_role(int(old_role_id))
                        if old_role:
                            try:
                                await guild.get_member(int(user_id)).remove_roles(old_role)
                            except disnake.Forbidden:
                                print(f"Не удалось удалить роль {old_role_id} у пользователя {user_id} на сервере {guild.id}")

            new_role_ids = roles.get(status, [])
            if new_role_ids:
                for guild in bot.guilds:
                    member = guild.get_member(int(user_id))
                    if member:
                        for new_role_id in new_role_ids:
                            new_role = guild.get_role(int(new_role_id))
                            if new_role:
                                try:
                                    await member.add_roles(new_role)
                                except disnake.Forbidden:
                                    print(f"Не удалось добавить роль {new_role_id} пользователю {user_id} на сервере {guild.id}")

            user_data['status'] = status
            user_data['status_expiration'] = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
            user_data['rewards'] -= prices[status]
            data[user_id] = user_data
            save_data(data)

            await inter.response.send_message(f"Вы купили статус: **@{status}**!", ephemeral=True)
        else:
            await handle_individual_status_request(inter)

    @tasks.loop(hours=24)
    async def check_status_expiration():
        now = datetime.now(timezone.utc)
        data = load_data()

        for user_id, user_data in data.items():
            expiration_str = user_data.get('status_expiration')
            if expiration_str:
                expiration = datetime.fromisoformat(expiration_str).astimezone(timezone.utc)
                if now > expiration:
                    role_ids = ROLES.get(user_data.get('status'))
                    if role_ids:
                        for guild in bot.guilds:
                            member = guild.get_member(int(user_id))
                            if member:
                                for role_id in role_ids:
                                    role = guild.get_role(int(role_id))
                                    if role:
                                        try:
                                            await member.remove_roles(role)
                                        except disnake.Forbidden:
                                            print(f"Не удалось удалить роль {role_id} у пользователя {user_id} на сервере {guild.id}")
                    user_data['status'] = None
                    user_data['status_expiration'] = None
                    data[user_id] = user_data

        save_data(data)

    def load_data():
        try:
            with open('admin/user_data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(data):
        with open('admin/user_data.json', 'w') as file:
            json.dump(data, file, indent=4)

    check_status_expiration.start()




