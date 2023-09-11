import asyncio
from contextlib import suppress

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from amplitude import Amplitude

from src.bot.config import read_config
from src.bot.handlers import router
from src.bot.middlewares import DatabaseMiddleware


async def main():
    config = read_config('config.ini')
    pool = await asyncpg.create_pool(config.postgres.dsn)
    db_mw = DatabaseMiddleware(pool)
    ampl = Amplitude(config.amplitude.api_token)
    dp = Dispatcher()
    dp['ampl'] = ampl
    dp['webapp'] = config.telegram.webapp
    dp.include_router(router)
    dp.message.middleware(db_mw)
    bot = Bot(config.telegram.token)
    await bot.set_my_commands([
        BotCommand(command='menu', description='New character choice'),
        BotCommand(command='start', description='Introduction')
    ])
    await dp.start_polling(bot)


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
