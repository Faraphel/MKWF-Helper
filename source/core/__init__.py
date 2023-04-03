from .browser import init as browser_init
from .discord import init as discord_init
from .dolphin import run as dolphin_run
from source.settings import Settings


def start(settings: Settings):
    discord_init()  # initialise the discord module TODO: what if pypresence crash ?
    browser_init(settings.browser)  # initialize the browser module

    # run the dolphin monitoring and process
    dolphin_run(settings.dolphin_executable_path, settings.dolphin_data_path)
