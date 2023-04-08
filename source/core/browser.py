import subprocess
from pathlib import Path
from typing import Final

from selenium import webdriver

from source import WEBSITE_URL

driver = None


AVAILABLE_BROWSERS: Final[list[str]] = [
    "chrome",
    "edge"
]

BROWSER_PATH: Final[Path] = Path("./browser")
BROWSER_DRIVER_PATH: Final[Path] = BROWSER_PATH / "driver"
BROWSER_DRIVER_PATH.mkdir(exist_ok=True, parents=True)
BROWSER_USER_PATH: Final[Path] = BROWSER_PATH / "user"
BROWSER_USER_PATH.mkdir(exist_ok=True, parents=True)


def init(browser: str = "chrome"):
    match browser:
        case "edge": init_edge()
        case _: init_chrome()


def init_chrome():
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    init_chromium_type(
        name="chrome",
        driver_cls=webdriver.Chrome,
        options=Options(),
        service=Service(str(BROWSER_DRIVER_PATH / "chromedriver.exe")),
    )


def init_edge():
    global driver

    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.edge.service import Service

    init_chromium_type(
        name="edge",
        driver_cls=webdriver.Edge,
        options=Options(),
        service=Service(str(BROWSER_DRIVER_PATH / "msedgedriver.exe")),
    )


def init_chromium_type(name: str, driver_cls, options, service):
    global driver

    options.add_argument(f"app={WEBSITE_URL}")  # start in a window without tabs
    options.add_argument(f"user-data-dir={(BROWSER_USER_PATH / name).absolute()}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # disable the "automated" message

    service.creation_flags = subprocess.CREATE_NO_WINDOW  # hide the devtool shell

    driver = driver_cls(service=service, options=options)
