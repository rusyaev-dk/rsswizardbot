from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from l10n.translator import LocalizedTranslator


def main_menu_kb(l10n: LocalizedTranslator):
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text=l10n.get_text(key="example-btn")),
    ]

    builder.add(*buttons)
    # builder.adjust(1, 2, 3)
    return builder.as_markup(resize_keyboard=True)
