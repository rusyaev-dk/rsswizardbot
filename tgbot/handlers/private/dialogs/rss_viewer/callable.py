from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from infrastructure.database.repositories.rss_repo import RSSRepository
from l10n.translator import Translator
from tgbot.keyboards.reply import main_menu_kb
from tgbot.misc.states import ViewRssSG


@inject
async def fetch_user_rss(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        rss_repo: FromDishka[RSSRepository]
):
    user_rss_list = await rss_repo.get_all_user_rss(owner_tg_id=call.from_user.id)
    return [
        rss.rss_url for rss in user_rss_list
    ]


@inject
async def close_feed_viewer(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        l10n: FromDishka[Translator]
):
    await call.message.delete()
    await call.message.answer(l10n.get_text(key='main-menu-msg'),
                              reply_markup=main_menu_kb(l10n))

    await dialog_manager.done()
    await dialog_manager.reset_stack()


@inject
async def select_rss_feed(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        rss_id: str,
        l10n: FromDishka[Translator],
        rss_repo: FromDishka[RSSRepository]
):
    rss = await rss_repo.get_rss_by_id(rss_id=rss_id)

    dialog_manager.dialog_data["selected_rss_id"] = rss_id
    dialog_manager.dialog_data["current_page"] = 1

    entries, status_code = await rss_repo.get_rss_entries(rss_url=rss.rss_url)
    if status_code != 200:
        dialog_manager.dialog_data["status_code"] = status_code
        await dialog_manager.switch_to(ViewRssSG.VIEW_FEED_ERROR)
        return

    dialog_manager.dialog_data["entries"] = entries
    await dialog_manager.switch_to(ViewRssSG.VIEW_FEED)


@inject
async def delete_rss(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        l10n: FromDishka[Translator],
        rss_repo: FromDishka[RSSRepository]
):
    rss_id = dialog_manager.dialog_data.get("selected_rss_id")
    await rss_repo.delete_rss(owner_tg_id=call.from_user.id, rss_id=rss_id)

    dialog_manager.dialog_data["selected_rss_id"] = None
    await call.answer(text=l10n.get_text(key="rss-deleted-msg"), show_alert=False)

    dialog_manager.dialog_data["current_page"] = 1

    user_rss_list = await rss_repo.get_all_user_rss(owner_tg_id=call.from_user.id)
    if not user_rss_list:
        await call.message.delete()
        await call.message.answer(l10n.get_text(key="main-menu-msg"),
                                  reply_markup=main_menu_kb(l10n))
        await dialog_manager.done()
        await dialog_manager.reset_stack()
        return

    await dialog_manager.switch_to(ViewRssSG.SELECT_RSS)


async def prev_page(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    current_page = dialog_manager.dialog_data.get("current_page", 1)
    if current_page == 1:
        await call.answer()
        return

    dialog_manager.dialog_data["current_page"] = current_page - 1
    await dialog_manager.switch_to(ViewRssSG.VIEW_FEED)


async def next_page(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    current_page = dialog_manager.dialog_data.get("current_page", 1)
    total_pages = dialog_manager.dialog_data.get("total_pages", 1)

    if current_page == total_pages:
        await call.answer()
        return

    dialog_manager.dialog_data["current_page"] = current_page + 1
    await dialog_manager.switch_to(ViewRssSG.VIEW_FEED)


async def cancel_feed_viewer(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data["current_page"] = 1
    await dialog_manager.switch_to(ViewRssSG.SELECT_RSS)
