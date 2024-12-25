from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SetUserLanguageFactory(CallbackData, prefix="set_language"):
    language_code: str


def set_user_language_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Русский", callback_data=SetUserLanguageFactory(language_code="ru"))
    builder.button(text="🇬🇧 English", callback_data=SetUserLanguageFactory(language_code="en"))

    builder.adjust(2)

    return builder.as_markup()
