from aiogram import types, Router, F, flags
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from l10n.translator import Translator
from tgbot.keyboards.reply import main_menu_kb
from tgbot.misc.constants import CANCEL_BUTTONS

echo_router = Router()


@echo_router.message(StateFilter(None))
@flags.rate_limit(key="default")
@echo_router.message(F.text, StateFilter(None))
@inject
async def bot_echo(
        message: types.Message,
        state: FSMContext,
        l10n: FromDishka[Translator]
):
    if message.text in CANCEL_BUTTONS:
        await state.clear()
        await message.answer(l10n.get_text(key="main-menu-msg"),
                             reply_markup=main_menu_kb(l10n))
    return
