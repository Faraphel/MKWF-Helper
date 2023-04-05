from typing import Final

GITHUB_REPO: Final[str] = "Faraphel/MKWF-Helper"
GITHUB_ROOT_URL: Final[str] = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/"
GITHUB_RELEASES_URL: Final[str] = f"https://github.com/{GITHUB_REPO}/releases/"


from .update import new_version_available  # NOQA
