import argparse

from source import core, OPTION_PATH
from source.settings import Settings


def run(args: argparse.Namespace, settings: Settings):
    settings.dolphin_executable_path = args.dolphin_executable_path
    settings.dolphin_data_path = args.dolphin_data_path
    settings.browser = args.browser

    settings.save_to(OPTION_PATH)

    core.start(settings)
