from aiogram.types.user import User
from aiogram_i18n.managers import BaseManager


class I18nManager(BaseManager):
    async def get_locale(self, event_from_user: User) -> str:
        lang_code = event_from_user.language_code or self.default_locale
        return lang_code
    async def set_locale(self, locale: str, event_from_user: User):
        pass