import disnake
from disnake.ext import commands
import json
import os

def setup_all_initiative(bot: commands.Bot):
    @bot.slash_command(name='list_projects', description='Показать список всех проектов.')
    async def list_projects(inter: disnake.ApplicationCommandInteraction):
        projects = load_projects()
        embed = disnake.Embed(
            title="🌟 Список всех проектов 🌟",
            description="Вот крутые и прибыльные проекты. Нажмите на кнопки, чтобы узнать больше.",
        )
        
        view = disnake.ui.View()
        button_names = ["1", "2", "3", "4", "5"]
        
        for idx, (project_name, info) in enumerate(projects.items()):
            if project_name == 'creator_support':
                continue
            description = info.get("description", "Описание отсутствует.")
            main_link = info.get("main_link", "Ссылка отсутствует.")
            embed.add_field(
                name=f"**> {project_name}**",
                value=f"```{description}```",
                inline=False
            )
            button = disnake.ui.Button(label=button_names[idx], url=main_link)
            view.add_item(button)

        await inter.send(embed=embed, view=view)


    @bot.slash_command(name='creator_support', description='Поддержать создателя донатом.')
    async def creator_support(inter: disnake.ApplicationCommandInteraction):
        projects = load_projects()
        creator_info = projects.get('creator_support', {})
        description = creator_info.get("description", "Описание отсутствует.")
        dpn_link = creator_info.get("dpn_link", "Ссылка отсутствует.")
        dpo_link = creator_info.get("dpo_link", "Ссылка отсутствует.")
        
        embed = disnake.Embed(
            title="Поддержка создателя!",
            description=description,
        )
        
        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(label="Donationalerts", url=dpn_link))
        view.add_item(disnake.ui.Button(label="Patreon", url=dpo_link))
        
        await inter.send(embed=embed, view=view)

    @bot.slash_command(name='list_details', description='Получить более подробную информацию о проекте.')
    async def list_details(inter: disnake.ApplicationCommandInteraction, проект: str = commands.Param(choices=["Game Quest", "Nanson", "ANIME INDUSTRY", "KINO INDUSTRY", "Стримус"])):
        projects = load_projects()
        project_info = projects.get(проект, {})
        if not project_info:
            await inter.send(f"Проект с названием {проект} не найден.")
            return
        
        description = project_info.get("description", "Описание отсутствует.")
        web_link = project_info.get("web_link", "Ссылка отсутствует.")
        youtube_link = project_info.get("youtube_link", "Ссылка на YouTube отсутствует.")
        avatar_path = project_info.get("avatar", None)
        
        embed = disnake.Embed(
            title=f"Подробная информация о проекте {проект}"
        )
        embed.add_field(
            name="> Описание проекта:",
            value=f"```{description}```",
            inline=False
        )

        view = disnake.ui.View()
        if web_link and web_link != "Ссылка отсутствует.":
            view.add_item(disnake.ui.Button(label="Перейдите на веб-страницу", url=web_link))
        if youtube_link and youtube_link != "Ссылка на YouTube отсутствует.":
            view.add_item(disnake.ui.Button(label="Перейдите на YouTube-канал", url=youtube_link))

        if avatar_path and os.path.isfile(avatar_path):
            with open(avatar_path, 'rb') as avatar_file:
                avatar_image = disnake.File(avatar_file, filename="avatar.png")
                embed.set_thumbnail(url="attachment://avatar.png")
                embed.set_footer(text="Благодарим вас за интерес к проекту!")
                await inter.send(embed=embed, file=avatar_image, view=view)
        else:
            await inter.send(embed=embed, view=view)

def load_projects():
    try:
        with open('letproject/projects.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def setup(bot: commands.Bot):
    setup_all_initiative(bot)







