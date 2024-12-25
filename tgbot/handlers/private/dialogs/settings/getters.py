from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from l10n.translator import Translator


@inject
async def overall_settings_getter(
        dialog_manager: DialogManager,
        l10n: FromDishka[Translator],
        **kwargs
):
    data = {
        "choose_option_text": l10n.get_text(key='choose-option-msg'),
        "change_language_btn_text": l10n.get_text(key='change-language-btn'),
        "close_btn_text": l10n.get_text(key='close-btn')
    }

    return data


@inject
async def change_language_getter(
        dialog_manager: DialogManager,
        l10n: FromDishka[Translator],
        **kwargs
):
    data = {
        "back_btn_text": l10n.get_text(key='back-btn')
    }

    return data
