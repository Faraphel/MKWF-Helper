from source import gui, OPTION_PATH
from source.settings import Settings

settings = Settings.load_from(OPTION_PATH)


window = gui.Window(settings)
window.mainloop()

# TODO: update detection ?
# TODO: propose to enable / disable the discord RPC
# TODO: cli
