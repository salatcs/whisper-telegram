from aiogram import Bot, F, Router
from aiogram.types import (
    ChosenInlineResult,
    InlineQuery,
    InlineQueryResultArticle,
    InlineQueryResultsButton,
    InputTextMessageContent,
)
from aiogram_i18n import I18nContext
from asyncpg.connection import Connection

from ..db.functions import check_name, create_whisper, get_most_users
from ..parse_tools import parse_whisper_query
from ..keyboards import whisper_keyboard

router = Router(name=__name__)

async def send_default(inline_query: InlineQuery, bot: Bot, i18n: I18nContext):
    me = await bot.get_me()
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id="how_send",
                title=i18n.get("add-username"),
                description=i18n.get("format-whisper", bot_username=me.username),
                input_message_content=InputTextMessageContent(message_text=i18n.get("inline-instruction-whisper"))
            )
        ],
        button=InlineQueryResultsButton(text=i18n.get("how-send-whisper"), start_parameter="start"),
        cache_time=1
    )

@router.inline_query(
    F.query, F.query.strip().split()[-1].startswith("@") | F.query.strip().split()[-1].isdigit()
)
async def whisper_handler(inline_query: InlineQuery, bot: Bot, session: Connection, i18n: I18nContext):
    request = parse_whisper_query(inline_query.query)

    if not request:
        await send_default(inline_query, bot, i18n)
        return
    
    db_name = await check_name(request.target_id, request.target_username, session)
    
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id=f"whisper:{request.target}",
                title=i18n.get("create-whisper", target=db_name),
                description=i18n.get("create-whisper-description"),
                input_message_content=InputTextMessageContent(message_text=i18n.get("whisper-text", target=db_name)),
                reply_markup=whisper_keyboard(i18n)
            )
        ],
        cache_time=1
    )

@router.inline_query(F.query.strip())
async def whisper_without_username_handler(inline_query: InlineQuery, bot: Bot, session: Connection, i18n: I18nContext):
    if len(" ".join(inline_query.query.split()[:-1])) > 200:
        await send_default(inline_query, bot, i18n)
        return
    
    users = await get_most_users(inline_query.from_user.id, session)
    
    results = [
        InlineQueryResultArticle(
            id=f"fast_whisper:{user['tg_id']}",
            title=i18n.get("create-whisper", target=user["name"] or user["username"] or user["tg_id"]),
            description=i18n.get("create-whisper-description"),
            input_message_content=InputTextMessageContent(message_text=i18n.get("whisper-text",
                                                          target=user["name"] or user["username"] or user["tg_id"])),
            reply_markup=whisper_keyboard(i18n)
        )
        for user in users
    ]
    
    me = await bot.get_me()
    
    results.append(
        InlineQueryResultArticle(
            id="how_send",
            title=i18n.get("add-username"),
            description=i18n.get("format-whisper", bot_username=me.username),
            input_message_content=InputTextMessageContent(message_text=i18n.get("inline-instruction-whisper"))
        )
    )
    
    await inline_query.answer(
        results=results,
        button=InlineQueryResultsButton(text=i18n.get("how-send-whisper"), start_parameter="start"),
        cache_time=1
    )

@router.chosen_inline_result(F.result_id.startswith("whisper"))
async def whisper_chosen_handler(inline_result: ChosenInlineResult, session: Connection):
    tg_id, username = None, None
    
    if inline_result.result_id.split(":")[-1].isdigit():
        tg_id = int(inline_result.result_id.split(":")[-1])
    else:
        username = inline_result.result_id.split(":")[-1]
    
    message = " ".join(inline_result.query.split()[:-1])
    
    await create_whisper(inline_result.from_user.id, tg_id, username, message, inline_result.inline_message_id, session)

@router.chosen_inline_result(F.result_id.startswith("fast_whisper"))
async def whisper_chosen_handler(inline_result: ChosenInlineResult, session: Connection):
    tg_id, username = None, None
    
    if inline_result.result_id.split(":")[-1].isdigit():
        tg_id = int(inline_result.result_id.split(":")[-1])
    else:
        username = inline_result.result_id.split(":")[-1]
    
    message = inline_result.query
    
    await create_whisper(inline_result.from_user.id, tg_id, username, message, inline_result.inline_message_id, session)

@router.inline_query()
async def bot_info_handler(inline_query: InlineQuery, bot: Bot, i18n: I18nContext):
    await send_default(inline_query, bot, i18n)