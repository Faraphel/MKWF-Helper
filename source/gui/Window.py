import webbrowser
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
import traceback

from source import core, OPTION_PATH, version
from source.settings import Settings
from source.version import GITHUB_RELEASES_URL


class Window(tk.Tk):
    def __init__(self, settings: Settings, *args, **kwargs):
        super().__init__(*args, **kwargs)

        new_version_available = version.new_version_available()

        if new_version_available:
            if messagebox.askyesno("Update", "A new version of MKWF-Helper is available. Do you want to install it ?"):
                webbrowser.open(GITHUB_RELEASES_URL)

        self.settings = settings

        self.title("MKWF-Helper")
        self.resizable(False, False)

        self.photoimage_icon = tk.PhotoImage(file="assets/icon.png")
        self.wm_iconphoto(True, self.photoimage_icon)

        self.frame_dolphin = FrameDolphin(self, text="Dolphin")
        self.frame_dolphin.grid(row=1, column=1, sticky=tk.NSEW)

        self.frame_browser = FrameBrowser(self, text="Browser")
        self.frame_browser.grid(row=2, column=1, sticky=tk.NSEW)

        self.button_start = ttk.Button(self, text="Start", width=10, command=self.start)
        self.button_start.grid(row=3, column=1, sticky=tk.E)

    def sync_settings(self):
        self.settings.dolphin_executable_path = self.frame_dolphin.path_dolphin_executable
        self.settings.dolphin_data_path = self.frame_dolphin.path_dolphin_data
        self.settings.browser = core.browser.AVAILABLE_BROWSERS[self.frame_browser.listbox_browser.current()]

        self.settings.save_to(OPTION_PATH)

    def start(self):
        self.sync_settings()  # synchronise and save the settings
        self.destroy()  # destroy the window

        try:
            core.start(self.settings)

        except Exception:  # NOQA
            messagebox.showerror(
                f"An error occurred",
                f"An error occurred while trying to start the application :\n\n{str(traceback.format_exc())}"
            )


class FrameDolphin(ttk.LabelFrame):
    def __init__(self, master: Window, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.label_dolphin_executable = ttk.Label(self, text="Executable path")
        self.entry_dolphin_executable = ttk.Entry(self, width=50)
        self.entry_dolphin_executable.insert(0, master.settings.dolphin_executable_path)
        self.button_dolphin_executable = ttk.Button(
            self, text="...", width=3,
            command=self.select_dolphin_executable
        )
        self.label_dolphin_executable.grid(row=1, column=1, sticky=tk.W)
        self.entry_dolphin_executable.grid(row=2, column=1)
        self.button_dolphin_executable.grid(row=2, column=2)

        self.label_dolphin_data = ttk.Label(self, text="Data path")
        self.entry_dolphin_data = ttk.Entry(self, width=50)
        self.entry_dolphin_data.insert(0, master.settings.dolphin_data_path)
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


class FrameBrowser(ttk.LabelFrame):
    def __init__(self, master: Window, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.listbox_browser = ttk.Combobox(self, values=core.browser.AVAILABLE_BROWSERS)
        self.listbox_browser.set(master.settings.browser)
        self.listbox_browser.grid(row=1, column=1)
