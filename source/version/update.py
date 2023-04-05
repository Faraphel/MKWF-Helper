from typing import Optional

import requests
from requests import RequestException

from source.version import GITHUB_ROOT_URL


def str_to_version(text: str) -> list[int]:
    return [int(x) for x in text.split(".")]


def get_current_version() -> str:
    with open("./version") as file:
        return file.read()


def get_latest_version() -> Optional[str]:
    try:
        request = requests.get(GITHUB_ROOT_URL + "version", timeout=5)
    except RequestException:  # if can't connect to the website
        return None

    if request.status_code != 200:  # if the request didn't work correctly
        return None

    return request.content.decode()


def new_version_available() -> bool:
    latest_version = get_latest_version()
    if latest_version is None: return False
    current_version = get_current_version()

    return str_to_version(latest_version) > str_to_version(current_version)
