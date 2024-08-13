import disnake
from disnake.ext import commands

def setup_questionnaires_profile(bot: commands.Bot):
    @bot.slash_command(name='creator_profile', description='Просмотреть анкету создателя.')
    async def creator_profile(inter: disnake.ApplicationCommandInteraction):
        avatar_url = "https://cdn.discordapp.com/attachments/963534892082290688/1267128099405828227/photo_2023-03-02_18-59-23.jpg"  # URL для аватарки
        banner_url = "https://cdn.discordapp.com/attachments/963534892082290688/1267128077117292655/FaS7iOhBBW0.jpg"  # URL для баннера
        description = (
            "Я — молодой человек с неиссякаемой страстью к творчеству. Мое сердце принадлежит созданию видео и написанию захватывающих сценариев. "
            "Моя истинная страсть — программное обеспечение, такое как Adobe Photoshop, Adobe After Effects, Adobe Premiere Pro и многие другие. "
            "Эти инструменты помогают мне создавать увлекательные видеоролики, которые не только привлекают внимание, но и оставляют незабываемые впечатления в сердцах зрителей.\n\n"
            "Но мое творчество не ограничивается только видео. В мире программирования я также в совершенстве владею языком Python. С его помощью я создаю разнообразные Discord-боты и веб-сайты, воплощая свои идеи в жизнь.\n\n"
            "Однако это еще далеко не все! Изучая электрические системы и электротехнику, я погружаюсь в глубокие технические аспекты этой области.\n\n"
            "Я ищу человека, который так же, как и я, живет творчеством и вдохновением. Прекрасно проведенное время в приятной компании — вот что всегда было важно для меня."
        )
        multisite_link = "https://andremuhamed.nexcord.pro/multilink/creator/torex"
        personal_website = "https://andremuhamed.nexcord.pro/"

        embed = disnake.Embed(
            title="Анкета создателя — Андрей Мухамед",
            description=description,
        )
        embed.set_thumbnail(url=avatar_url)
        embed.set_image(url=banner_url)

        buttons = disnake.ui.ActionRow()
        buttons.add_button(
            label="Мультиссылка",
            url=multisite_link,
            style=disnake.ButtonStyle.link
        )
        buttons.add_button(
            label="Личный веб-сайт",
            url=personal_website,
            style=disnake.ButtonStyle.danger
        )

        embed.set_footer(text="Спасибо, что верите в автора!")

        await inter.send(embed=embed, components=[buttons])


