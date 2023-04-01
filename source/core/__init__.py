from .browser import init as browser_init
from .discord import init as discord_init
from .dolphin import run as dolphin_run


def init():
    browser_init()
    discord_init()
