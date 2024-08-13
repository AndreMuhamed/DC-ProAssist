import disnake
from disnake.ext import commands

class LayoutFixer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.eng_to_rus = {
            'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', 
            '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 
            'l': 'д', ';': 'ж', '\'': 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', 
            ',': 'б', '.': 'ю', '/': '.', '`': 'ё', 'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 
            'U': 'Г', 'I': 'Ш', 'O': 'Щ', 'P': 'З', '{': 'Х', '}': 'Ъ', 'A': 'Ф', 'S': 'Ы', 'D': 'В', 'F': 'А', 
            'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д', ':': 'Ж', '"': 'Э', 'Z': 'Я', 'X': 'Ч', 'C': 'С', 
            'V': 'М', 'B': 'И', 'N': 'Т', 'M': 'Ь', '<': 'Б', '>': 'Ю', '?': ',', '~': 'Ё'
        }

    def fix_layout(self, text):
        return ''.join([self.eng_to_rus.get(c, c) for c in text])

    @commands.slash_command(name='fixlayout', description='Восстанавливает русскую фразу, при включенной английской раскладке.')
    async def fix_layout_command(self, inter: disnake.ApplicationCommandInteraction, текст: str):
        """Восстанавливает русскую фразу, случайно набранную при включенной английской раскладке."""
        fixed_text = self.fix_layout(текст)

        # Создание эмбеда с двумя полями и GIF
        embed = disnake.Embed(
            title="<:Stickerus20:1269746218548858991> Исправление раскладки!",
            description="Вот как ваш текст выглядит после исправлений, внесённых нашим замечательным ботом.",
        )
        embed.add_field(name="Исходный текст:", value=текст, inline=False)
        embed.add_field(name="Исправленный текст:", value=fixed_text, inline=False)
        embed.set_thumbnail(url="https://i.gifer.com/3OoDx.gif")  # Замените на URL вашей GIF

        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(LayoutFixer(bot))
