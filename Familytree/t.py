import pickledb
import disnake
from disnake.ext import commands
import itertools

class Tree(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='tree', description='Показать семейное дерево пользователя.')
    async def tree(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
        if member is None:
            member = inter.author

        db = pickledb.load('Familytree/database.txt', False)

        class Person:
            ID = itertools.count()
            def __init__(self, name, parent=None, level=0):
                self.id = next(self.__class__.ID)
                self.parent = parent
                self.name = name
                self.level = level
                self.children = []

        def create_tree(d, parent=None, level=0):
            if d:
                person = Person(d['parent'], parent, level)
                level += 1
                person.children = [create_tree(child, person, level) for child in d['children']]
                return person

        def get_children(parent):
            final_children = []
            children = db.get(f"{parent}child").split("|/")
            children = [child for child in children if child]

            for child in children:
                if child == parent:
                    continue  # Пропускаем самоссылки

                partner = ""
                if db.exists(f"{child}partner"):
                    partner = " + " + db.get(f"{child}partner")

                child_tree = {
                    'parent': child + partner,
                    'children': get_children(child) if db.exists(f"{child}child") else []
                }
                final_children.append(child_tree)
            return final_children

        no_family_response = "У этого пользователя нет семьи :("
        author = member
        if not (db.exists(f"{author.name}partner") or db.exists(f"{author.name}child")):
            return await inter.send(no_family_response)

        partner = db.get(f"{author.name}partner") if db.exists(f"{author.name}partner") else ""
        if db.exists(f"{author.name}child"):
            family_tree = {
                'parent': f"{author.name}" + (" + " + partner if partner else ""),
                'children': get_children(f"{author.name}")
            }
        else:
            family_tree = {
                'parent': f"{author.name}" + (" + " + partner if partner else ""),
                'children': []
            }

        def format_tree(parent, indent=0):
            result = ' ' * (indent * 2) + parent.name + '\n'
            for child in parent.children:
                result += format_tree(child, indent + 1)
            return result

        tree_root = create_tree(family_tree)
        tree_output = format_tree(tree_root).strip()

        # Создание embed сообщения
        embed = disnake.Embed(title=f"Семейное дерево — {member.name}", description=f"```\n{tree_output}\n```")
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url="https://i.gifer.com/3OoSR.gif")  # Гифка в качестве изображения

        # Отправка сообщения с embed
        await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(Tree(bot))




