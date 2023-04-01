import pypresence


presence = pypresence.Presence(1091407271466127361)


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
