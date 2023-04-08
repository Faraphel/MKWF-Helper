# MKWF-Helper

MKWF-Helper is a tool designed to allow you to see in real time on which track you are playing on the website https://faraphel.fr.
This allows you to easily give a score to the current track, see information, post a comment, and every other features available on the website.  
If you have discord installed on your computer, it will also show a custom Rich Presence containing the name of the current track you are playing on.  

Despite the name of the tool being MKWF-Helper, it can work on any Mario Kart Wii game or mods, not only MKWF.

# Requirements

You need to have [Dolphin](https://fr.dolphin-emu.org) installed and either 
[Google Chrome](https://www.google.com/intl/fr_fr/chrome/) or 
[Microsoft Edge](https://www.microsoft.com/fr-fr/edge/download?form=MA13FJ).

Currently, the mod only support Windows. Linux support will be added in a future version.

# Installation

Go in the [releases](https://github.com/Faraphel/MKWF-Helper/releases) page and simply download the latest version.  
If a new version of the tool is released, a pop-up will appear when starting the application.

# Usage

The tool can be used in two different way :
- with the graphical user interface (GUI)
- with the command line interface (CLI)

The settings used are saved to the `option.json` file and will be used as default values for the next usage.

## GUI

- Enter the path to your Dolphin executable (Dolphin.exe file)
- Enter your Dolphin data directory (can be located either in your %AppData% directory or your Documents)
- Select your preferred web browser and press start.

Dolphin should now start with another window showing the main page of MKWF.

## CLI

The command line interface accept the following arguments :
- `--dolphin-executable / -de` : the path to the dolphin executable
- `--dolphin-data / -da` : the path to your dolphin data directory
- `--browser / -b` : the browser to use

Dolphin should now start with another window showing the main page of MKWF.

# Issue

If you encounter an issue, you can go on the [MKWF's discord](https://discord.gg/HEYW5v8ZCd) to report it, or open an
issue on the GitHub page.
