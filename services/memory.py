from services.loggers import logger
from services.loggers_config import get_logger

# Словарь для хранения истории переписки
user_buffer_memory = dict()


# Очистка контекстной памяти диалога
async def clear_id_memory(user_id: int):
    try:
        global user_buffer_memory
        del user_buffer_memory[user_id]
        logger.info(
            f"Cleared context memory for user_id: {user_id}")
    except Exception as ex:
        logger.critical(f'Error clear for user {user_id}: {ex}')