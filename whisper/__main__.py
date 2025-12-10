import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from asyncpg import create_pool

from .config import settings
from .functions import apply_middleware_to_all, include_all_routers, init_logging
from .middlewares import I18nManager, InitUserMiddleware, SessionMiddleware

init_logging()

bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Localization
i18n_middleware = I18nMiddleware(
    core=FluentRuntimeCore(
        path="whisper/locales/{locale}"
    ),
    default_locale=settings.DEFAULT_LOCALE,
    manager=I18nManager()
)
i18n_middleware.setup(dispatcher=dp)


apply_middleware_to_all(dp, InitUserMiddleware())
include_all_routers(dp)

async def main():
    pool = await create_pool(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        min_size=settings.MIN_POOL_SIZE,
        max_size=settings.MAX_POOL_SIZE
    )
    
    apply_middleware_to_all(dp, SessionMiddleware(pool))
    
    await dp.start_polling(bot, pool=pool)

if __name__ == "__main__":
    asyncio.run(main())