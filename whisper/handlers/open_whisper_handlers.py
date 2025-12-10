from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext
from asyncpg import Connection

from ..db.functions import find_whisper

router = Router(name=__name__)

@router.callback_query(F.data == "open_whisper")
async def open_whisper_handler(callback: CallbackQuery, session: Connection, i18n: I18nContext):
    whisper = await find_whisper(callback.inline_message_id, session)
    can_open = (callback.from_user.id in {whisper["from_id"], whisper["to_id"]}) \
        or (callback.from_user.username == whisper["to_username"])

    if not can_open:
        await callback.answer(i18n.get("no-access-whisper"), show_alert=True)
    else:
        await callback.answer(whisper["text"], show_alert=True)