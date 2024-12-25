import html

from aiogram import Router, flags
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from infrastructure.database.repositories.users_repo import UsersRepository
from l10n.translator import Translator
from tgbot.keyboards.inline import SetUserLanguageFactory
from tgbot.keyboards.reply import main_menu_kb
from tgbot.services.setup_bot_commands import update_user_commands

start_router = Router()


@start_router.message(CommandStart())
@flags.rate_limit(key="default")
@inject
async def bot_start(
        message: Message,
        state: FSMContext,
        l10n: FromDishka[Translator]
):
    await state.clear()
    args = {
        "name": html.escape(message.from_user.full_name)
    }

    text = l10n.get_text(key="hello-msg", args=args)

    await message.answer(text, reply_markup=main_menu_kb(l10n=l10n), disable_web_page_preview=True)


@start_router.callback_query(SetUserLanguageFactory.filter())
@inject
async def set_user_language(
        call: CallbackQuery,
        callback_data: SetUserLanguageFactory,
        users_repo: FromDishka[UsersRepository],
        l10n: FromDishka[Translator],
):
    language_code = callback_data.language_code

    await users_repo.add_user(
        telegram_id=call.from_user.id,
        full_name=call.from_user.full_name,
        language_code=language_code,
        username=call.from_user.username,
    )
    l10n.change_locale(language_code)
    await call.answer()
    await call.message.delete()
    await update_user_commands(bot=call.bot, l10n=l10n)
    args = {
        "name": html.escape(call.from_user.full_name)
    }
    text = l10n.get_text(key="hello-msg", args=args)
    await call.message.answer(text, reply_markup=main_menu_kb(l10n), disable_web_page_preview=True)
