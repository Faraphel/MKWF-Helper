from datetime import datetime
import os
import subprocess
import time
from pathlib import Path
from typing import Generator

from source import GameState, WEBSITE_URL


def get_logs(process, path: Path | str) -> Generator[str, None, None]:
    with open(path, "r") as file:
        file.seek(0, os.SEEK_END)

        while process.poll() is None:
            if not (line := file.readline()):
                time.sleep(1)
                continue

            yield line


def run(dolphin_executable_path: Path, dolphin_data_path: Path):
    from .browser import driver
    from .discord import presence

    process = subprocess.Popen(
        [
            dolphin_executable_path,

            "--user", dolphin_data_path,

            "--config=Logger.Options.Verbosity=4",  # enable all type of logs
            "--config=Logger.Options.WriteToFile=True",  # write the logs into a file

            "--config=Logger.Logs.BOOT=True",  # enable the BOOT logs (path to the game)
            "--config=Logger.Logs.CORE=True",  # enable the CORE logs (ID of the game)
            "--config=Logger.Logs.FileMon=True",  # enable the FileMon logs (loaded and unloaded files)
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    def on_track_changed(self: GameState):
        driver.get(f"{WEBSITE_URL}/mkwf/track/{self.track_sha1}")

        presence.update(
            state="Playing",
            details=self.track_name,
            start=int(datetime.now().timestamp()),
            large_image="icon"
        )

    game_state = GameState()
    game_state.add_listener("track_changed", on_track_changed)

    for line in get_logs(process, dolphin_data_path / "Logs/dolphin.log"):
        game_state.update_from_log(line)
