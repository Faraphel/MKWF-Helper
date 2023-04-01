import os
from pathlib import Path
from tkinter import ttk, filedialog
import tkinter as tk

from source import core

DEFAULT_DOLPHIN_EXECUTABLE: Path = Path(os.getenv("ProgramFiles")) / "Dolphin/Dolphin.exe"
DEFAULT_DOLPHIN_DATA: Path = Path(os.getenv("AppData")) / "Dolphin Emulator"


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("MKWF-Helper")
        self.resizable(False, False)

        self.frame_dolphin = FrameDolphin(self, text="Dolphin")
        self.frame_dolphin.grid(row=1, column=1)

        self.button_start = ttk.Button(self, text="Start", width=10, command=self.start)
        self.button_start.grid(row=2, column=1, sticky=tk.E)

    def start(self):
        # get the executable and data path before destroying the window to keep the values
        executable, data = self.frame_dolphin.path_dolphin_executable, self.frame_dolphin.path_dolphin_data
        self.destroy()  # destroy the window
        core.init()  # initialise the core of the tool
        core.dolphin.run(executable, data)  # run the dolphin monitoring and process


class FrameDolphin(ttk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_dolphin_executable = ttk.Label(self, text="Chemin de l'exécutable")
        self.entry_dolphin_executable = ttk.Entry(self, width=50)
        self.entry_dolphin_executable.insert(0, str(DEFAULT_DOLPHIN_EXECUTABLE))
        self.button_dolphin_executable = ttk.Button(
            self, text="...", width=3,
            command=self.select_dolphin_executable
        )
        self.label_dolphin_executable.grid(row=1, column=1, sticky=tk.W)
        self.entry_dolphin_executable.grid(row=2, column=1)
        self.button_dolphin_executable.grid(row=2, column=2)

        self.label_dolphin_data = ttk.Label(self, text="Chemin des données")
        self.entry_dolphin_data = ttk.Entry(self, width=50)
        self.entry_dolphin_data.insert(0, str(DEFAULT_DOLPHIN_DATA))
        self.button_dolphin_data = ttk.Button(
            self, text="...", width=3,
            command=self.select_dolphin_data
        )
        self.label_dolphin_data.grid(row=3, column=1, sticky=tk.W)
        self.entry_dolphin_data.grid(row=4, column=1)
        self.button_dolphin_data.grid(row=4, column=2)

    def select_dolphin_executable(self):
        path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if not path: return
        path = Path(path)

        self.entry_dolphin_executable.delete(0, tk.END)
        self.entry_dolphin_executable.insert(0, str(path))

    def select_dolphin_data(self):
        path = filedialog.askdirectory()
        if not path: return
        path = Path(path)

        self.entry_dolphin_data.delete(0, tk.END)
        self.entry_dolphin_data.insert(0, str(path))

    @property
    def path_dolphin_executable(self) -> Path:
        return Path(self.entry_dolphin_executable.get())

    @property
    def path_dolphin_data(self) -> Path:
        return Path(self.entry_dolphin_data.get())
