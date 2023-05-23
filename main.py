import argparse

from source import gui, OPTION_PATH, cli
from source.settings import Settings

settings = Settings.load_from(OPTION_PATH)


parser = argparse.ArgumentParser()
parser.add_argument("--cli", dest="gui", action="store_false", help="Don't use the graphical interface")

cli.load_arguments(parser, settings)
args = parser.parse_args()


if args.gui:
    window = gui.Window(settings)
    window.mainloop()
else:
    cli.run(args, settings)

# TODO: twitch integration ?
# TODO: handle error with a popup or a log
