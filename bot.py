import asyncio
import logging
import os
from pathlib import Path

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.database.setup import create_engine, create_session_pool
from l10n.translator import TranslatorHub
from tgbot.config import load_config, Config
from tgbot.handlers import routers_list
from tgbot.middlewares.database import OuterDatabaseMiddleware, InnerDatabaseMiddleware, UserExistingMiddleware
from tgbot.middlewares.l10n import L10nMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.misc.constants import DEFAULT_THROTTLE_TIME
from tgbot.services import broadcaster


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


def get_storage(config):
    """
    Return storage based on the provided configuration.

    Args:
        config (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


def setup_translator(
    locales_dir_path: str
) -> TranslatorHub:

    all_files = os.listdir(locales_dir_path + "/ru")
    fluent_files = [file for file in all_files if file.endswith(".ftl")]

    translator_hub = TranslatorHub(
        locales_dir_path=str(locales_dir_path), locales=["ru", "uz", "en"],
        resource_ids=fluent_files
    )
    return translator_hub


def register_global_middlewares(
        dp: Dispatcher,
        translator_hub: TranslatorHub,
        session_pool: async_sessionmaker,
):
    dp.message.outer_middleware(OuterDatabaseMiddleware(session_pool))
    dp.callback_query.outer_middleware(OuterDatabaseMiddleware(session_pool))

    dp.message.middleware(ThrottlingMiddleware(
        default_throttle_time=DEFAULT_THROTTLE_TIME))

    dp.message.middleware(InnerDatabaseMiddleware())
    dp.callback_query.middleware(InnerDatabaseMiddleware())

    dp.message.middleware(UserExistingMiddleware())

    dp.message.middleware(L10nMiddleware(translator_hub))
    dp.callback_query.middleware(L10nMiddleware(translator_hub))


# def setup_scheduling(
#         scheduler: AsyncIOScheduler,
#         bot: Bot,
#         config: Config,
#         translator_hub: TranslatorHub,
#         session_pool: async_sessionmaker
# ):


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Bot started!")


async def main():
    setup_logging()

    config = load_config(".env")
    storage = get_storage(config)
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

    # Localization initialization:
    locales_dir_path = Path(__file__).parent.joinpath("l10n/locales")
    translator_hub = setup_translator(locales_dir_path=str(locales_dir_path))

    # Routers and dialogs initialization:
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers_list)
    # setup_dialogs(dp)
    dp.workflow_data.update(config=config, translator_hub=translator_hub)

    # Database initialization:
    engine = create_engine(db=config.db)
    session_pool = create_session_pool(engine=engine)

    # Middlewares initialization:
    register_global_middlewares(
        dp=dp,
        translator_hub=translator_hub,
        session_pool=session_pool
    )

    # Scheduling initialization:
    # scheduler = AsyncIOScheduler()
    # setup_scheduling()

    await on_startup(bot, config.tg_bot.admin_ids)
    # scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Stopping bot")
