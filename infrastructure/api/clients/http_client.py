import ssl

import aiohttp
import certifi
from aiohttp import TCPConnector


class HttpClient:
    def __init__(self):
        """
        Initializing an HTTP client with an aiohttp session.
        """

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)
        self.__session = aiohttp.ClientSession(connector=connector)

    async def make_request(
            self,
            url: str,
            method: str = "GET",
            headers: dict = None,
            params: dict = None
    ) -> str:
        async with self.__session.request(method, url, headers=headers, params=params) as response:
            response.raise_for_status()

            # Проверяем MIME-тип ответа
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/json" in content_type:
                return await response.json()
            elif any(ct in content_type for ct in [
                "application/rss+xml",  # RSS-ленты
                "application/xml",  # Общий XML
                "text/xml",  # Устаревший XML
                "application/atom+xml"  # Atom-ленты
            ]):
                return await response.text()
            else:
                raise ValueError(f"Unsupported content type: {content_type}")

    async def close(self):
        await self.__session.close()
