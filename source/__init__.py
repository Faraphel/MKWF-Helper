from pathlib import Path
from typing import Final


# Constantes (before the local import to avoid infinite import)
WEBSITE_URL: Final[str] = "https://faraphel.fr"

CACHE_PATH: Final[Path] = Path(".cache/")
CACHE_PATH.mkdir(exist_ok=True)


from .GameState import GameState  # NOQA


