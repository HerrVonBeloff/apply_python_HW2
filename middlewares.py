from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        # Логируем входящее событие
        if event.message:
            logger.info(f"Получено сообщение: {event.message.text} от пользователя {event.message.from_user.id}")
        else:
            logger.info(f"Получено событие типа: {event.update_type}")

        return await handler(event, data)