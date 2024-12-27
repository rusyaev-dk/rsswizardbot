import asyncio
import logging
import ssl

import aiohttp
import feedparser

from infrastructure.api.clients.http_client import HttpClient
from tgbot.services.micro_functions import clean_summary, truncate_text


class RSSClient:
    def __init__(
            self,
            http_client: HttpClient,
    ):
        self.__http_client = http_client
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

    async def get_entries(
            self,
            rss_url: str,
    ) -> tuple[list[dict], int]:
        try:
            rss_text = await self.__http_client.make_request(rss_url, method="GET", headers=None, params=None)

            feed = feedparser.parse(rss_text)
            entries = []

            for entry in feed.entries:
                link = self.extract_link(entry)
                cleaned_summary = clean_summary(entry.get("summary", ""))
                entries.append({
                    "title": truncate_text(entry.get("title", ""), max_length=250),
                    "short_summary": truncate_text(cleaned_summary, max_length=250),
                    "link": link
                })

            return entries, 200  # success

        except aiohttp.client_exceptions.ClientResponseError as e:
            logging.error(f"HTTP error: {e.status} — {e.message}")
            return [], e.status

        except aiohttp.client_exceptions.ClientConnectorError:
            logging.error("Connection error: server is unavailable.")
            return [], 503  # 503 Service Unavailable

        except feedparser.exceptions.CharacterEncodingOverride:
            logging.error("Character encoding error in the RSS feed.")
            return [], 422  # 422 Unprocessable Entity

        except ValueError:
            logging.error("Invalid RSS feed format.")
            return [], 400  # 400 Bad Request

        except asyncio.TimeoutError:
            logging.error("Request timeout: the server took too long to respond.")
            return [], 504  # 504 Gateway Timeout

        except KeyError as e:
            logging.error(f"Invalid RSS feed structure. Missing key: {e}")
            return [], 422  # 422 Unprocessable Entity

        except Exception as e:
            logging.error(f"Unknown error: {e}")
            return [], -1

    async def validate_rss(
            self,
            rss_url: str
    ) -> tuple[bool, int]:
        try:
            rss_text = await self.__http_client.make_request(rss_url, method="GET", headers=None, params=None)
            feed = feedparser.parse(rss_text)
            return bool(feed.bozo == 0 and feed.entries and feed.feed.title), 200

        except aiohttp.client_exceptions.ClientResponseError as e:
            logging.error(f"HTTP error: {e.status} — {e.message}")
            return False, e.status

        except aiohttp.client_exceptions.ClientConnectorError:
            logging.error("Connection error: server is unavailable.")
            return False, 503  # 503 Service Unavailable

        except feedparser.exceptions.CharacterEncodingOverride:
            logging.error("Character encoding error in the RSS feed.")
            return False, 422  # 422 Unprocessable Entity

        except ValueError:
            logging.error("Invalid RSS feed format.")
            return False, 400  # 400 Bad Request

        except asyncio.TimeoutError:
            logging.error("Request timeout: the server took too long to respond.")
            return False, 504  # 504 Gateway Timeout

        except KeyError as e:
            logging.error(f"Invalid RSS feed structure. Missing key: {e}")
            return False, 422  # 422 Unprocessable Entity

        except Exception as e:
            logging.error(f"Unknown error: {e}")
            return False, -1

    @staticmethod
    def extract_link(entry: dict) -> str:
        """
        Извлекает ссылку из RSS-записи.
        """

        if "links" in entry and isinstance(entry["links"], list):
            for link in entry["links"]:
                if "href" in link:
                    return link["href"]

        if "id" in entry:
            return entry["id"]

        return "No link available"
