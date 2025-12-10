from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

from ..config import settings
from ..db.functions import init_db_user

class InitUserMiddleware(BaseMiddleware):
    cache = TTLCache(maxsize=settings.MAX_TTLCACHE_SIZE, ttl=3600)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: User = getattr(event, "from_user", None)

        if user:
            current_data = (user.username, user.full_name)
            
            cached_data = self.cache.get(user.id)

            if cached_data != current_data:
                await init_db_user(
                    tg_id=user.id,
                    username=user.username,
                    name=user.full_name,
                    session=data['session']
                )
                self.cache[user.id] = current_data

        return await handler(event, data)