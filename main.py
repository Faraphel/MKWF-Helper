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


DOLPHIN_EXECUTABLE: Path = Path(r"C:\Program Files\Dolphin\Dolphin.exe")
DOLPHIN_DATA: Path = Path(os.getenv("AppData")) / "Dolphin Emulator"


process = subprocess.Popen(
    [
        DOLPHIN_EXECUTABLE,

        "--config=Logger.Options.Verbosity=4",  # enable all type of logs
        "--config=Logger.Options.WriteToFile=True",  # write the logs into a file

        "--config=Logger.Logs.BOOT=True",  # enable the BOOT logs (path to the game)
        "--config=Logger.Logs.CORE=True",  # enable the CORE logs (ID of the game)
        "--config=Logger.Logs.FileMon=True",  # enable the FileMon logs (loaded and unloaded files)

        "--config=Dolphin.General.UseDiscordPresence=False",  # disable dolphin discord presence
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

driver_service = Service("./driver/chromedriver.exe")  # TODO: other service than chrome
driver_options = Options()
driver_options.add_argument("--app=https://faraphel.fr")  # start in a window without tabs
driver_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # disable the "automated" message

driver = webdriver.Chrome(service=driver_service, options=driver_options)

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


for line in get_logs(DOLPHIN_DATA / "Logs/dolphin.log"):
    game_state.update_from_log(line)
