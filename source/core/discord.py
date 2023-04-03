import pypresence


APPLICATION_ID: int = 1091407271466127361


presence = pypresence.Presence(APPLICATION_ID)


def init():
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
