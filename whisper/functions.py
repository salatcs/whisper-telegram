import logging
from typing import Union

from aiogram import BaseMiddleware, Dispatcher, Router

from .config import settings
from .handlers import (
    inline_query_handlers,
    lifespan_handlers,
    open_whisper_handlers,
    pm_bot_handlers,
)

def apply_middleware_to_all(router: Union[Dispatcher, Router], middleware: BaseMiddleware):
    for i in dir(router):
        attr = getattr(router, i)
        if "outer_middleware" in dir(attr):
            attr.outer_middleware(middleware)

def include_all_routers(router: Union[Dispatcher, Router]):
    router.include_routers(lifespan_handlers.router, inline_query_handlers.router, open_whisper_handlers.router,
                           pm_bot_handlers.router)

def init_logging():
    log_format = "%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"
    log_level = logging.INFO

    handlers = []

    if settings.LOGGING_MODE == "only_file":
        handlers.append(logging.FileHandler("whisper.log", encoding="utf-8"))

    elif settings.LOGGING_MODE == "only_stdout":
        handlers.append(logging.StreamHandler())

    elif settings.LOGGING_MODE == "all":
        handlers.append(logging.FileHandler("whisper.log", encoding="utf-8"))
        handlers.append(logging.StreamHandler())

    else:
        handlers.append(logging.StreamHandler())
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )
    
    logging.getLogger('aiogram.event').propagate = False