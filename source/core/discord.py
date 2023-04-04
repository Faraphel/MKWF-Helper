import pypresence
from pypresence import DiscordNotFound

APPLICATION_ID: int = 1091407271466127361


presence = None


try:
    presence = pypresence.Presence(APPLICATION_ID)
except DiscordNotFound:
    pass


def init():
    if presence is None: return  # if it is not possible to connect to discord, ignore

    presence.connect()
    presence.update(
        buttons=[
            {
                "label": "Get MKWF",
                "url": "https://github.com/Faraphel/MKWF-Install"
            }, {
                "label": "Get MKWF-Helper",
                "url": "https://github.com/Faraphel/MKWF-Helper"
            }
        ]
    )
