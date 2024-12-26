from .bot_start import start_router
from .main_menu import menu_router
from .commands.user_commands import user_commands_router
from .commands.admin_commands import admin_commands_router
from .dialogs.rss_viewer.dialogs import rss_dialog
from .dialogs.settings.dialogs import settings_dialog

private_routers = [
    start_router,
    admin_commands_router,
    user_commands_router,
    menu_router,
    rss_dialog,
    settings_dialog
]

__all__ = [
    "private_routers",
]
