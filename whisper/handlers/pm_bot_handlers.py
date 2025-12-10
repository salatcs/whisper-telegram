from aiogram import Bot, F, Router, html
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext, LazyProxy as L
from asyncpg import Connection

from ..db.functions import add_in_bot
from ..keyboards import request_user_kb, send_whisper_kb, start_kb
from ..parse_tools import validate_target

router = Router(name=__name__)

router.message.filter(F.chat.type == "private")

@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, session: Connection, i18n: I18nContext):
    await add_in_bot(message.from_user.id, session)
    me = await bot.get_me()
    await message.answer(
        i18n.get("hello-message", full_name=html.quote(message.from_user.full_name), bot_username=me.username),
        reply_markup=start_kb(i18n)
    )

@router.callback_query(F.data == "mode_select_user")
async def ask_contact_handler(callback: CallbackQuery, i18n: I18nContext):
    await callback.message.delete()
    await callback.message.answer(
        i18n.get("request-user-msg"),
        reply_markup=request_user_kb(i18n)
    )

@router.message(F.user_shared)
async def user_shared_handler(message: Message, bot: Bot, i18n: I18nContext):
    user_id = str(message.user_shared.user_id)
    me = await bot.get_me()
    
    await message.answer(
        i18n.get("hello-message", full_name=html.quote(message.from_user.full_name), bot_username=me.username),
        reply_markup=start_kb(i18n)
    )
    
    await message.answer(
        i18n.get("generate-whisper-btn", target=user_id),
        reply_markup=send_whisper_kb(str(user_id), i18n)
    )

@router.message(F.text == L("btn-cancel"))
async def cancel_handler(message: Message, bot: Bot, i18n: I18nContext):
    me = await bot.get_me()
    await message.answer(
        i18n.get("hello-message", full_name=html.quote(message.from_user.full_name), bot_username=me.username),
        reply_markup=start_kb(i18n)
    )

@router.message(F.text)
async def text_input_handler(message: Message, session: Connection, i18n: I18nContext):
    target = validate_target(message.text.strip())
    
    if target:
        await message.answer(
            i18n.get("generate-whisper-btn", target=target),
            reply_markup=send_whisper_kb(target, i18n)
        )
    else:
        await message.answer(i18n.get("user-not-found"))