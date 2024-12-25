from aiogram import Router, flags, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from infrastructure.database.repositories.rss_repo import RSSRepository
from l10n.translator import Translator
from tgbot.keyboards.reply import main_menu_kb, cancel_kb
from tgbot.misc.constants import SETTINGS_BUTTONS, ADD_RSS_BUTTONS, VIEW_FEED_BUTTONS, CANCEL_BUTTONS
from tgbot.misc.states import SettingsSG, ViewRssSG, AddRssSG
from tgbot.services.micro_functions import format_error_message

menu_router = Router()


@menu_router.message(F.text.in_(ADD_RSS_BUTTONS))
@flags.rate_limit(key="default")
@inject
async def add_rss(
        message: Message,
        state: FSMContext,
        dialog_manager: DialogManager,
        l10n: FromDishka[Translator]
):
    await dialog_manager.reset_stack()
    await state.set_state(AddRssSG.GET_RSS_URL)
    await message.answer(l10n.get_text(key="send-url-msg"), reply_markup=cancel_kb(l10n))


@menu_router.message(AddRssSG.GET_RSS_URL)
@flags.rate_limit(key="default")
@inject
async def process_rss_url(
        message: Message,
        state: FSMContext,
        l10n: FromDishka[Translator],
        rss_repo: FromDishka[RSSRepository]
):
    if message.text in CANCEL_BUTTONS:
        await message.answer(l10n.get_text("action-canceled-msg"),
                             reply_markup=main_menu_kb(l10n))
        await state.clear()
        return

    msg = await message.answer(l10n.get_text(key="processing-msg"))

    rss_url = message.text.strip()

    exists = await rss_repo.is_rss_exists(owner_tg_id=message.from_user.id, rss_url=rss_url)
    if exists:
        await msg.delete()
        await message.answer(l10n.get_text(key="rss-already-exists-msg"),
                             reply_markup=main_menu_kb(l10n))
        await state.clear()
        return

    valid, status_code = await rss_repo.validate_rss(rss_url)
    if not valid:
        await msg.delete()
        text = format_error_message(status_code=status_code, l10n=l10n)
        await message.answer(text, reply_markup=main_menu_kb(l10n))
        await state.clear()
        return

    await msg.delete()
    await rss_repo.add_rss(rss_url=rss_url, owner_tg_id=message.from_user.id)
    await message.answer(l10n.get_text(key="rss-added-msg"), reply_markup=main_menu_kb(l10n))
    await state.clear()


@menu_router.message(F.text.in_(VIEW_FEED_BUTTONS))
@flags.rate_limit(key="default")
@inject
async def view_feed(
        message: Message,
        dialog_manager: DialogManager,
        l10n: FromDishka[Translator],
        rss_repo: FromDishka[RSSRepository]
):
    user_rss_list = await rss_repo.get_all_user_rss(owner_tg_id=message.from_user.id)

    if not user_rss_list:
        await message.answer(l10n.get_text(key="no-feeds-msg"))
        return

    await dialog_manager.start(ViewRssSG.SELECT_RSS, mode=StartMode.RESET_STACK)


@menu_router.message(F.text.in_(SETTINGS_BUTTONS))
@flags.rate_limit(key="default")
async def settings(
        message: Message,
        dialog_manager: DialogManager
):
    await dialog_manager.start(
        state=SettingsSG.OVERALL_SETTINGS,
        mode=StartMode.RESET_STACK,
    )
