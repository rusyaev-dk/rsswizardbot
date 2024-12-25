from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo,  Row
from aiogram_dialog.widgets.text import Format, Const

from tgbot.handlers.private.dialogs.settings.getters import overall_settings_getter, change_language_getter
from tgbot.handlers.private.dialogs.settings.callable import change_user_language, close_settings
from tgbot.misc.constants import SET_USER_LANGUAGE_TEXT
from tgbot.misc.states import SettingsSG

overall_settings_window = Window(
    Format("{choose_option_text}"),
    SwitchTo(
        text=Format("{change_language_btn_text}"),
        id="btn_go_to_change_language",
        state=SettingsSG.CHANGE_LANGUAGE
    ),
    Button(
        text=Format("{close_btn_text}"),
        id="btn_close_settings",
        on_click=close_settings
    ),
    getter=overall_settings_getter,
    state=SettingsSG.OVERALL_SETTINGS
)


change_user_language_window = Window(
    Const(SET_USER_LANGUAGE_TEXT),
    Row(
        Button(
            text=Const("🇷🇺 Русский"),
            id="btn_set_language_ru",
            on_click=change_user_language
        ),
        Button(
            text=Const("🇬🇧 English"),
            id="btn_set_language_en",
            on_click=change_user_language
        ),
    ),
    SwitchTo(
        text=Format("{back_btn_text}"),
        id="btn_cancel_language_setting",
        state=SettingsSG.OVERALL_SETTINGS
    ),
    getter=change_language_getter,
    state=SettingsSG.CHANGE_LANGUAGE
)

settings_dialog = Dialog(
    overall_settings_window,
    change_user_language_window
)
