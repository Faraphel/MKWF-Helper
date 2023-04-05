import argparse

from source import core, OPTION_PATH, version
from source.settings import Settings
from source.version import GITHUB_RELEASES_URL


def run(args: argparse.Namespace, settings: Settings):
    settings.dolphin_executable_path = args.dolphin_executable_path
    settings.dolphin_data_path = args.dolphin_data_path
    settings.browser = args.browser

    settings.save_to(OPTION_PATH)

    if version.new_version_available():
        print(f"A new version is available at {GITHUB_RELEASES_URL}")

    core.start(settings)
