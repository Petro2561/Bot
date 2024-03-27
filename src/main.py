import sys
import logging
import asyncio

from aiogram import Bot, Dispatcher
from config import Config, load_config
from aiogram.fsm.storage.memory import MemoryStorage

logger = logging.getLogger(__name__)


async def main():    
    logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
            '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    config: Config = load_config()
    bot = Bot(token=config.bot_token.get_secret_value())
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')