
from .private import private_routers
from .echo import echo_router

routers_list = [
    *private_routers,
    echo_router,
]

__all__ = [
    "routers_list",
]
