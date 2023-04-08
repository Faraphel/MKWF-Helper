from pathlib import Path
from typing import Final


# Constantes (before the local import to avoid infinite import)
WEBSITE_URL: Final[str] = "https://faraphel.fr/mkwf"
WEBSITE_TRACK_URL: Final[str] = f"{WEBSITE_URL}/track"

CACHE_PATH: Final[Path] = Path(".cache/")
CACHE_PATH.mkdir(exist_ok=True)

TOOLS_PATH: Final[Path] = Path("tools/")
OPTION_PATH: Final[Path] = Path("option.json")


from .GameState import GameState  # NOQA


