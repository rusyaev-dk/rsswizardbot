from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from l10n.translator import Translator
from tgbot.config import Config

user_commands_router = Router()


@user_commands_router.message(Command("help"))
@flags.rate_limit(key="default")
@inject
async def get_help(
        message: Message,
        l10n: FromDishka[Translator],
        config: FromDishka[Config]
):
    await message.answer(l10n.get_text(key="help-msg",
                                       args={"support_username": config.tg_bot.support_username}))
