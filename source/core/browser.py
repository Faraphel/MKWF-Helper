import subprocess
from http import HTTPStatus
from io import BytesIO
from pathlib import Path
from typing import Final
from zipfile import ZipFile

import requests
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


def download_driver(base_url: str, driver_prefix: str, driver_filename: str, executable_path: Path, version_path: Path):
    """
    :param base_url: The base url for the download
    :param driver_prefix: the prefix used in the url
    :param driver_filename: the filename of the executable file
    :param executable_path: the path where the executable will be downloaded
    :param version_path: the path to the version file of the executable
    """

    # try to get the latest driver available
    try:
        request = requests.get(f"{base_url}/LATEST_RELEASE", timeout=5)

        if request.status_code == HTTPStatus.OK:
            # get the latest version
            version: str = request.content.decode()

            # if the current version does not exist or the version is different
            if not version_path.exists() or version != version_path.read_text():

                # download the driver
                request = requests.get(f"{base_url}/{version}/{driver_prefix}_win32.zip")

                if request.status_code == HTTPStatus.OK:
                    # load a zip file from the downloaded content
                    with BytesIO(request.content) as stream, ZipFile(stream) as zipfile:
                        # extract the file into the driver directory
                        executable_path.write_bytes(zipfile.read(driver_filename))
                        version_path.write_text(version)

    # ignore if the requests timed out
    except requests.exceptions.ReadTimeout:
        pass


def init_chrome():
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    # set the driver path
    driver_directory_path: Final[Path] = BROWSER_DRIVER_PATH / "chrome"
    driver_directory_path.mkdir(exist_ok=True)
    driver_executable_path: Final[Path] = driver_directory_path / "driver.exe"
    driver_version_path: Final[Path] = driver_directory_path / "version"

    # download the driver
    download_driver(
        base_url="https://chromedriver.storage.googleapis.com",
        driver_prefix="chromedriver",
        driver_filename="chromedriver.exe",
        executable_path=driver_executable_path,
        version_path=driver_version_path,
    )

    # initialise the driver as chromium like
    init_chromium_type(
        name="chrome",
        driver_cls=webdriver.Chrome,
        options=Options(),
        service=Service(str(driver_executable_path)),
    )


def init_edge():
    global driver

    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.edge.service import Service

    # set the driver path
    driver_directory_path: Final[Path] = BROWSER_DRIVER_PATH / "edge"
    driver_directory_path.mkdir(exist_ok=True)
    driver_executable_path: Final[Path] = driver_directory_path / "driver.exe"
    driver_version_path: Final[Path] = driver_directory_path / "version"

    # download the driver
    download_driver(
        base_url="https://msedgedriver.azureedge.net",
        driver_prefix="edgedriver",
        driver_filename="msedgedriver.exe",
        executable_path=driver_executable_path,
        version_path=driver_version_path,
    )

    # initialise the driver as chromium like
    init_chromium_type(
        name="edge",
        driver_cls=webdriver.Edge,
        options=Options(),
        service=Service(str(BROWSER_DRIVER_PATH / "msdedriver.exe")),
    )


def init_chromium_type(name: str, driver_cls, options, service):
    global driver

    options.add_argument(f"app={WEBSITE_URL}")  # start in a window without tabs
    options.add_argument(f"user-data-dir={(BROWSER_USER_PATH / name).absolute()}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # disable the "automated" message

    service.creation_flags = subprocess.CREATE_NO_WINDOW  # hide the devtool shell

    driver = driver_cls(service=service, options=options)
