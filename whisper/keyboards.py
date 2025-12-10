from aiogram.types import InlineKeyboardButton, KeyboardButton, KeyboardButtonRequestUser
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram_i18n import I18nContext

def whisper_keyboard(i18n: I18nContext):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=i18n.get("open-whisper"),
            callback_data="open_whisper"
        )
    )
    return kb_builder.as_markup()

def start_kb(i18n: I18nContext):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=i18n.get("btn-select-user-mode"),
            callback_data="mode_select_user"
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text=i18n.get("btn-manual-mode"),
            switch_inline_query="... @"
        )
    )
    return kb_builder.as_markup()

def request_user_kb(i18n: I18nContext):
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(
        KeyboardButton(
            text=i18n.get("btn-request-user"),
            request_user=KeyboardButtonRequestUser(
                request_id=1,
                user_is_bot=False
            )
        )
    )
    kb_builder.row(
        KeyboardButton(text=i18n.get("btn-cancel"))
    )
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def send_whisper_kb(target: str, i18n: I18nContext):
    kb_builder = InlineKeyboardBuilder()
    query_text = f"... @{target}" 
    
    kb_builder.row(
        InlineKeyboardButton(
            text=i18n.get("generate-whisper-btn", target=target),
            switch_inline_query=query_text
        )
    )
    return kb_builder.as_markup()