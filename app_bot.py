import traceback
import disnake
from disnake.ext import commands
from features.profile_commands import setup_profile_commands
from features.voice_tracker import setup_voice_tracker
from features.rewards_commands import setup_rewards_commands
from features.message_rewards import setup as setup_message_rewards
from features.checkinfo_commands import setup as setup_checkinfo
from features.currency_commands import setup_currency_commands
from features.status_commands import setup_status_commands
from features.marriage_commands import setup as setup_marriagecommands
from admin.error_log import handle_exception, log_error
from admin.data_handler import load_data, save_data, ensure_user_profile
from supecomma.managemen import setup_managemen
from supecomma.status_bot import setup as setup_statusbot
from supecomma.techno_comand import setup_test_command
from supecomma.lottery_button import setup as setup_lottery
from supecomma.suggestion_commands import setup as setup_suggestioncommands
from supecomma.config import BOT_TOKEN
from specialwith.individual import setup as setup_individual
from specialwith.gamequest_news import setup as setup_gamequest_news
from specialwith.muhamed import setup as setup_muhamed
from user_tops.top_commands import setup as setup_topcommands
from user_tops.avatar_commands import setup_avatar_commands
from user_tops.banner_commands import setup_banner_commands  
from letproject.questionnaires_profile import setup_questionnaires_profile
from letproject.alinitiative import setup_all_initiative
from entertainment.youtube_music import setup_music_commands
from entertainment.magic_commands import setup_magic_commands
from entertainment.layout_fixer import setup as setup_layout_fixer
from bomessage.auto_reply import send_auto_reply
from bomessage.welcome import setup as setup_welcome_command
from bomessage.mention_response import setup as setup_mention_response
from bomessage.reminder_sender import setup as setup_reminder_sender
from bomessage.periodic_messages import setup_periodic_tasks
from bomessage.farewell import setup as setup_farewell_command

intents = disnake.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Загрузка данных бота
data = load_data()
setup_statusbot(bot)

# Загрузка основных команд
setup_profile_commands(bot)
setup_voice_tracker(bot)
setup_rewards_commands(bot)
setup_message_rewards(bot)
setup_currency_commands(bot)
setup_marriagecommands(bot)
setup_status_commands(bot)
setup_managemen(bot)

# Розваги пользователей
setup_music_commands(bot)
setup_magic_commands(bot)
setup_layout_fixer(bot)
setup_test_command(bot)
setup_lottery(bot)

# Топ пользователи и их оформление
setup_topcommands(bot)
setup_avatar_commands(bot)
setup_banner_commands(bot)
setup_checkinfo(bot)

# Сообщения от бота
setup_welcome_command(bot)
setup_farewell_command(bot)
setup_periodic_tasks(bot)
setup_mention_response(bot)
setup_reminder_sender(bot)
setup_suggestioncommands(bot)

# Загрузка проектов создателя
setup_questionnaires_profile(bot)
setup_all_initiative(bot)

# Особые команды
setup_individual(bot)
setup_gamequest_news(bot)
setup_muhamed(bot)

@bot.event
async def on_message(message: disnake.Message):
    """Обрабатывает сообщения пользователей."""
    if message.author.bot:
        return

    # Создаем профиль при первом взаимодействии
    ensure_user_profile(data, str(message.author.id)) 

    # Обработка команд и сообщений в DMs
    if message.content.startswith('!'):
        await bot.process_commands(message)
        await message.delete()
    elif isinstance(message.channel, disnake.DMChannel):
        await send_auto_reply(message, data, str(message.author.id))
    else:
        await bot.process_commands(message)

    # Сохранение данных пользователя
    save_data(data) 

@bot.event
async def on_command_error(ctx, error):
    """Обрабатывает ошибки команд и записывает их в файл."""
    handle_exception(error) 

    if isinstance(error, commands.CommandNotFound):
        embed = disnake.Embed(
            title="<:Stickerus5:1269746098809864232> Команда не найдена!",
            description=f"Извините, команда `{ctx.message.content}` **не распознана**.",
        )
        embed.add_field(name="Подсказка:", value="Start all over, but it's not accurate.")
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/963534892082290688/1269283846956781578/626a7fb9f5861b9f.png')
        await ctx.author.send(embed=embed)

@bot.event
async def on_error(event_method, *args, **kwargs):
    if args:
        if isinstance(args[0], Exception):
            error_message = ''.join(traceback.format_exception(*args)) 
            log_error(error_message)
            print(f"An error occurred in {event_method}: {error_message}")
        else:
            print(f"An unexpected error occurred in {event_method}: {args[0]}")
    else:
        print(f"An unexpected error occurred in {event_method}: No additional information")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

bot.run(BOT_TOKEN)
