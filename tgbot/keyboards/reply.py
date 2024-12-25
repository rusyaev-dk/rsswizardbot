from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from l10n.translator import Translator


def main_menu_kb(l10n: Translator):
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text=l10n.get_text(key="add-rss-btn")),
        KeyboardButton(text=l10n.get_text(key="view-feed-btn")),
        KeyboardButton(text=l10n.get_text(key="settings-btn")),
    ]

    builder.add(*buttons)
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def cancel_kb(l10n: Translator):
    builder = ReplyKeyboardBuilder()
    builder.button(text=l10n.get_text(key="cancel-btn"))
    return builder.as_markup(resize_keyboard=True)
