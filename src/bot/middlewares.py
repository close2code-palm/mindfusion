from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from asyncpg import Pool

from src.bot.services import Repository


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, pool: Pool):
        self._pool = pool

    async def __call__(
            self, handler: Callable[[types.Message or types.CallbackQuery,
                                     Dict[str, Any]], Awaitable[Any]],
            event: types.Message or types.CallbackQuery, data: Dict[str, Any]
    ):
        async with self._pool.acquire() as conn:
            data['db'] = Repository(conn)
            await handler(event, data)
            del data['db']
