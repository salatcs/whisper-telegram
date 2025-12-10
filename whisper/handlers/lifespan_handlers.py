import asyncio
import logging

from aiogram import Bot, Router
from asyncpg.pool import Pool

from ..db.models import init_db

router = Router(name=__name__)
logger = logging.getLogger(__name__)

@router.startup()
async def on_startup(bot: Bot):
    await init_db()
    me = await bot.get_me()
    logger.info("🚀 Bot @%s started", me.username)

@router.shutdown()
async def on_shutdown(bot: Bot, pool: Pool):
    me = await bot.get_me()
    logger.info("⏳ Closing pool...")
    try:
        await asyncio.wait_for(pool.close(), timeout=15)
        logger.info("✔️ Pool closed")
    except asyncio.TimeoutError:
        await pool.terminate()
        logger.info("⚠️ Pool terminated")
    logger.info("⛔️ Bot @%s stopped", me.username)