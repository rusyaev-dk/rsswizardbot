from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from infrastructure.database.repositories.users_repo import UsersRepository
from tgbot.filters.admin import AdminFilter
# from tgbot.keyboards.inline import set_target_language_code_kb
# from tgbot.misc.states import NotifyUsersSG
from tgbot.services.micro_functions import format_statistics_info

admin_commands_router = Router()
admin_commands_router.message.filter(AdminFilter())


@admin_commands_router.message(Command("statistics"))
@flags.rate_limit(key="default")
@inject
async def get_bot_statistics(
        message: Message,
        users_repo: FromDishka[UsersRepository]
):
    text = await format_statistics_info(users_repo=users_repo)
    await message.answer(text)


# @admin_commands_router.message(Command("notify_users"))
# async def notify_users(
#         message: Message,
#         state: FSMContext
# ):
#     await message.answer("Настройка рассылки.", reply_markup=ReplyKeyboardRemove())
#     await message.answer("Укажите аудиторию:", reply_markup=set_target_language_code_kb())
#     await state.set_state(NotifyUsersSG.get_target_language_code)

