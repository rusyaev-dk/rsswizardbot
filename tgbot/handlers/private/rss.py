from aiogram import Router, flags
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from infrastructure.database.repositories.rss_repo import RSSRepository
import feedparser

from tgbot.misc.states import ViewRssSG

rss_router = Router()


@rss_router.message(Command("add_rss"))
@flags.rate_limit(key="default")
@inject
async def add_rss(
        message: Message,
        command: CommandObject,
        rss_repo: FromDishka[RSSRepository]
):
    if not command.args:
        await message.answer("Пожалуйста, укажите URL RSS-ленты.")
        return

    rss_url = command.args
    await rss_repo.add_rss(owner_tg_id=message.from_user.id, rss_url=rss_url)
    await message.answer(f"RSS-лента добавлена ✅")


@rss_router.message(Command("rss"))
@flags.rate_limit(key="default")
@inject
async def start_rss_dialog(
        message: Message,
        dialog_manager: DialogManager,
        rss_repo: FromDishka[RSSRepository]
):
    user_rss_list = await rss_repo.get_all_user_rss(owner_tg_id=message.from_user.id)
    if len(user_rss_list) == 0:
        await message.answer("У вас нет добавленных RSS-лент.")
        return

    await dialog_manager.start(ViewRssSG.SELECT_RSS, mode=StartMode.RESET_STACK)
