from .bot_start import start_router
from .main_menu import menu_router
from .dialogs.rss_viewer.dialogs import rss_dialog
from .dialogs.settings.dialogs import settings_dialog

private_routers = [
    start_router,
    menu_router,
    rss_dialog,
    settings_dialog
]

__all__ = [
    "private_routers",
]
