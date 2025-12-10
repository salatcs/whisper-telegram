from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from asyncpg import Pool

class SessionMiddleware(BaseMiddleware):
    def __init__(self, pool: Pool):
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.pool.acquire() as connection:
            data["session"] = connection
            return await handler(event, data)