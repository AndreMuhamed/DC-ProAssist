import traceback  
import disnake
from disnake.ext import commands
from features.profile_commands import setup_profile_commands
from features.sociability_commands import setup_profile_socials_commands
from features.voice_tracker import setup_voice_tracker
from features.rewards_commands import setup_rewards_commands
from features.message_rewards import setup as setup_message_rewards
from features.checkinfo_commands import setup as setup_checkinfo
from features.currency_commands import setup_currency_commands
from features.shop_status import setup_shop_status
from admin.error_log import handle_exception, log_error
from admin.data_handler import load_data, save_data, ensure_user_profile
from supecomma.managemen import setup_managemen
from supecomma.status_bot import setup as setup_statusbot
from supecomma.help_command import setup as setup_helpbotcommands
from supecomma.techno_comand import setup_test_command
from supecomma.lottery_button import setup as setup_lottery
from supecomma.suggestion_commands import setup as setup_suggestioncommands
from supecomma.server_info import setup as setup_serverinfo
from supecomma.emoj_info import setup as setup_emojinfo
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
from bomessage.welcome_commands import setup as setup_welcome_command
from bomessage.mention_response import setup as setup_mention_response
from bomessage.reminder_sender import setup as setup_reminder_sender
from bomessage.periodic_messages import setup_periodic_tasks
from bomessage.farewell_commands import setup as setup_farewell_command
from bomessage.handling_commands import setup as setup_errorhandlingCog

# Настройка intents
intents = disnake.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True
intents.guilds = True

# Загрузка данных бота
data = load_data()

# Основной блок
if __name__ == "__main__":
    bot = commands.Bot(command_prefix="!", intents=intents)      

    # Загрузка основных команд
    setup_profile_commands(bot)
    setup_profile_socials_commands(bot)
    setup_voice_tracker(bot)
    setup_rewards_commands(bot)
    setup_message_rewards(bot)
    setup_currency_commands(bot)
    setup_shop_status(bot)
    setup_managemen(bot)

    # Профиль бота
    setup_helpbotcommands(bot)
    setup_statusbot(bot)

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
    setup_errorhandlingCog(bot)
    setup_serverinfo(bot)
    setup_emojinfo(bot)

    # Загрузка проектов создателя
    setup_questionnaires_profile(bot)
    setup_all_initiative(bot)

    # Особые команды
    setup_individual(bot)
    setup_gamequest_news(bot)
    setup_muhamed(bot)

    @bot.event
    async def on_ready():
        print(f'Bot is online as {bot.user}!')

    @bot.event
    async def on_message(message: disnake.Message):
        """Обрабатывает сообщения пользователей."""
        if message.author.bot:
            return

        # Создаем профиль при первом взаимодействии
        ensure_user_profile(data, str(message.author.id)) 

        # Сохранение данных пользователя
        save_data(data) 

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

    bot.run(BOT_TOKEN)






