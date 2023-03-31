from datetime import datetime
from pathlib import Path
from typing import Generator

import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pypresence

from source import GameState

process = subprocess.Popen(
    [r"C:\Program Files\Dolphin\Dolphin.exe", "-d"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

driver = webdriver.Chrome(  # TODO: other service than chrome
    service=Service("./driver/chromedriver.exe"),
    options=Options()
)
driver.get("https://faraphel.fr")

presence = pypresence.Presence(1091407271466127361)
presence.connect()
presence.update(
    start=int(datetime.now().timestamp()),
    buttons=[
        {
            "label": "Download MKWF",
            "url": "https://github.com/Faraphel/MKWF-Install"
        }, {
            "label": "Download MKWF-Helper",
            "url": "https://github.com/Faraphel/MKWF-Helper"
        }
    ]
)


def get_logs(path: Path | str) -> Generator[str, None, None]:
    with open(path, "r") as file:
        file.seek(0, os.SEEK_END)

        while process.poll() is None:
            if not (line := file.readline()):
                time.sleep(1)
                continue

            yield line


def on_track_changed(self: GameState):
    driver.get(f"https://faraphel.fr/mkwf/track/{self.track_sha1}")

    presence.update(
        state="Playing",
        details=self.track_name,
    )


game_state = GameState()
game_state.add_listener("track_changed", on_track_changed)


for line in get_logs(r"C:\Users\RC606\Documents\Dolphin Emulator\Logs\dolphin.log"):
    game_state.update_from_log(line)
