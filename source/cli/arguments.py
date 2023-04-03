import argparse
from pathlib import Path

from source.core.browser import AVAILABLE_BROWSERS
from source.settings import Settings


def load_arguments(parser: argparse.ArgumentParser, settings: Settings):
    parser.add_argument(
        "-de", "--dolphin-executable",
        dest="dolphin_executable_path",
        type=Path, default=settings.dolphin_executable_path,
        help="The path to the Dolphin executable"

    )
    parser.add_argument(
        "-da", "--dolphin-data",
        dest="dolphin_data_path",
        type=Path, default=settings.dolphin_data_path,
        help="The path to the Dolphin data directory"
    )
    parser.add_argument(
        "-b", "--browser",
        dest="browser",
        choices=AVAILABLE_BROWSERS, default=settings.browser,
        help="The browser to use for the website"
    )
