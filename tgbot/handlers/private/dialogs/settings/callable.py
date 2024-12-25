import html

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from infrastructure.database.models import UserLocal
from infrastructure.database.repositories.users_repo import UsersRepository
from l10n.translator import Translator
from tgbot.keyboards.reply import main_menu_kb
from tgbot.services.setup_bot_commands import update_user_commands


@inject
async def close_settings(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        l10n: FromDishka[Translator]
):
    await call.message.edit_text(l10n.get_text(key='main-menu-msg'))
    await dialog_manager.done()
    await dialog_manager.reset_stack()


@inject
async def change_user_language(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        users_repo: FromDishka[UsersRepository],
        l10n: FromDishka[Translator]
):
    language_code = button.widget_id[-2:]
    l10n.change_locale(language_code)

    await users_repo.update_user(UserLocal.telegram_id == call.from_user.id, language_code=language_code)

    await dialog_manager.done()
    await dialog_manager.reset_stack()
    await call.message.delete()
    await update_user_commands(bot=call.bot, l10n=l10n)
    args = {
        "name": html.escape(call.from_user.full_name)
    }
    text = l10n.get_text(key="hello-msg", args=args)
    await call.message.answer(text, reply_markup=main_menu_kb(l10n), disable_web_page_preview=True)
