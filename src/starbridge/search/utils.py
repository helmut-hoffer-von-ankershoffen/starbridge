from urllib.parse import urlparse

import requests

# TODO: Import from client on update of bspc
from brave_search_python_client.constants import BASE_URL

from starbridge.utils import get_logger

logger = get_logger(__name__)


def is_connected():
    parsed = urlparse(BASE_URL)
    api_url = f"{parsed.scheme}://{parsed.netloc}/"
    try:
        response = requests.head(api_url, timeout=5)
        logger.info(
            f"Called head on {api_url}, got status_code: %s, final_url: %s",
            response.status_code,
            response.url,
        )
        return response.status_code in (200, 303)
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to connect to {api_url}: %s", e)
    return False
