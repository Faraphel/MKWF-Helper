import pickle
from pathlib import Path
from typing import Final

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from source import WEBSITE_URL

driver = None


BROWSER_PATH: Final[Path] = Path("./browser")
BROWSER_DRIVER_PATH: Final[Path] = BROWSER_PATH / "driver"
BROWSER_DRIVER_PATH.mkdir(exist_ok=True, parents=True)
BROWSER_USER_PATH: Final[Path] = BROWSER_PATH / "user"
BROWSER_USER_PATH.mkdir(exist_ok=True, parents=True)


def init():
    global driver

    # TODO: cookies

    driver_service = Service(str(BROWSER_DRIVER_PATH / "chromedriver.exe"))  # TODO: other service than chrome
    driver_options = Options()
    driver_options.add_argument(f"app={WEBSITE_URL}")  # start in a window without tabs
    driver_options.add_argument(f"user-data-dir={(BROWSER_USER_PATH / 'chrome').absolute()}")
    driver_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # disable the "automated" message

    driver = webdriver.Chrome(service=driver_service, options=driver_options)

