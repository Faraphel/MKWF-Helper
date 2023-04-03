import json
import os
from pathlib import Path
from typing import Any


class Settings:
    __slots__ = ("dolphin_executable_path", "dolphin_data_path", "browser")

    def __init__(
        self,
        dolphin_executable_path: Path = Path(os.getenv("ProgramFiles")) / "Dolphin/Dolphin.exe",
        dolphin_data_path: Path = Path(os.getenv("AppData")) / "Dolphin Emulator",
        browser: str = "chrome",
    ):
        self.dolphin_executable_path = Path(dolphin_executable_path)
        self.dolphin_data_path = Path(dolphin_data_path)
        self.browser = str(browser)

    def to_json(self) -> dict:
        data: dict[str, Any] = {}

        for name in self.__slots__:
            value = getattr(self, name)

            if isinstance(value, Path):
                value = str(value)

            data[name] = value

        return data

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)

    def save_to(self, path: Path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.to_json(), file, ensure_ascii=False)

    @classmethod
    def load_from(cls, path: Path):
        if not path.exists(): return cls()

        with open(path, "r", encoding="utf-8") as file:
            return cls.from_json(json.load(file))
