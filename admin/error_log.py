import logging
import json
import os
import traceback
from collections import defaultdict

error_log_file = 'admin/us_error_log.json'

# Настройка логгера
logger = logging.getLogger('error_logger')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(error_log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Чтение существующих ошибок из файла
def load_existing_errors():
    if not os.path.exists(error_log_file):
        return defaultdict(int)

    with open(error_log_file, 'r') as f:
        try:
            return defaultdict(int, json.load(f))
        except json.JSONDecodeError:
            return defaultdict(int)

# Запись ошибок в файл
def save_errors(errors):
    with open(error_log_file, 'w') as f:
        json.dump(errors, f, indent=4)

# Логирование ошибки с проверкой на дублирование
def log_error(error_message):
    errors = load_existing_errors()
    errors[error_message] += 1
    save_errors(errors)
    logger.error(error_message)

# Обработка исключений
def handle_exception(exc):
    error_message = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    log_error(error_message)







