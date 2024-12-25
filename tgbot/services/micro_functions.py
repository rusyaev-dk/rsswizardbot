import random
import string
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import html

from l10n.translator import Translator


def generate_random_id(length: int):
    """
    Generates random combination of symbols for questionnaire_id in database
    """

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(symbols) for _ in range(length))


def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def format_error_message(
        status_code: int,
        l10n: Translator
) -> str:
    key = f"code-{status_code}"
    text = l10n.get_text(key=key)
    if text[:5] == 'code-':
        text = l10n.get_text(key='unknown-error')
    return text


def clean_summary(summary: str) -> str:
    if not summary:
        return ""

    decoded_summary = html.unescape(summary)
    soup = BeautifulSoup(decoded_summary, "html.parser")
    cleaned_text = soup.get_text()

    return truncate_text(cleaned_text.strip(), max_length=250)


def truncate_text(text: str, max_length: int = 300) -> str:
    if len(text) > max_length:
        return text[:max_length].strip() + "..."
    return text
