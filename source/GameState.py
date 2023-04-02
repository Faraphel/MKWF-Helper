import re
import subprocess
from dataclasses import field, dataclass
from pathlib import Path
from typing import Optional
import requests

from . import WEBSITE_URL, CACHE_PATH
from .event import Event


@dataclass
class GameState(Event):
    game_path: Optional[Path] = field(default=None)
    game_id: Optional[str] = field(default=None)
    _track_id: Optional[int] = field(default=None)

    def __post_init__(self):
        super().__init__()

    # methods

    def is_mkw(self) -> bool:
        return self.game_id.startswith("RMC")

    def update_from_log(self, log: str):
        if (match := re.match(r".*Race/Course/(?P<track_id>[0-9a-f]{3})\.szs\n", log)) is not None:
            self.track_id = int(match.group("track_id"), 16)

        if (match := re.match(r".*Booting from disc: (?P<path>.*)\n", log)) is not None:
            self.game_path = Path(match.group("path"))

            if self.game_path.suffix == ".dol":
                # if FST game, go from ./sys/main.dol to ./
                self.game_path = self.game_path.parent.parent

        if (match := re.match(r".*Active title: (?P<id>.*)\n", log)) is not None:
            self.game_id = match.group("id")

    # properties

    @property
    def track_id(self) -> int:
        return self._track_id

    @track_id.setter
    def track_id(self, value: int):
        self._track_id = value
        if self.is_mkw():
            self.trigger_listener("track_changed")

    @property
    def track_path(self) -> Path:
        filename: str = f"{self.track_id:03x}.szs"
        subpath: str = f"files/Race/Course/{filename}"

        if self.game_path.is_dir():
            return self.game_path / subpath

        else:
            process = subprocess.run([
                "./tools/wit/wit",
                "EXTRACT",
                self.game_path,
                f"--files", f"+{subpath}",
                "--DEST", CACHE_PATH,
                "--flat",
                "--overwrite"
            ])
            if process.returncode != 0:
                raise Exception("Can't extract the file.")

            return Path(CACHE_PATH / filename)

    @property
    def track_sha1(self) -> str:
        return subprocess.run(  # TODO: wrapper ?
            ["./tools/szs/wszst", "SHA1", self.track_path],
            stdout=subprocess.PIPE
        ).stdout.decode().split(" ")[0]

    @property
    def track_url(self) -> str:
        return f"{WEBSITE_URL}/mkwf/track/{self.track_sha1}"

    @property
    def track_name(self) -> str:
        request = requests.get(self.track_url)

        if request.status_code != 200:
            return "- Unknown Track -"

        # TODO: make an api in faraphel.fr
        content: bytes = request.content
        title: bytes = content[content.find(b"<title>")+len(b"<title>"):content.rfind(b"</title>")]
        return title.split(b" - ")[-1].decode()

