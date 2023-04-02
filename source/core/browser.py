from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from source import WEBSITE_URL

driver = None


def init():
    global driver

    # TODO: cache

    driver_service = Service("browser/driver/chromedriver.exe")  # TODO: other service than chrome
    driver_options = Options()
    driver_options.add_argument(f"--app={WEBSITE_URL}")  # start in a window without tabs
    driver_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # disable the "automated" message

    driver = webdriver.Chrome(service=driver_service, options=driver_options)
