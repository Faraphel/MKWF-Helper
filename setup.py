from cx_Freeze import setup, Executable
import sys
from source.version import get_current_version

include_files = [
    "./LICENSE.md",
    "./README.md",
    "./version",

    "./assets",
    "./tools",

    sys.exec_prefix + "/DLLs/tcl86t.dll",
    sys.exec_prefix + "/DLLs/tk86t.dll",
]

options = {
    "build_exe": {
        "include_files": include_files,
        "includes": ["tkinter"],
        "packages": ["tkinter"],
        "include_msvcr": True,
    }
}

setup(
    options=options,
    name='MKWF-Helper',
    version=get_current_version(),
    url='https://github.com/Faraphel/MKWF-Helper',
    license='Apache-2.0',
    author='Faraphel',
    author_email='rc60650@hotmail.com',
    description='Mario Kart Wii Mod Helper.',
    executables=[
        Executable(
            "main.py",
            icon="./assets/icon.ico",
            # base="win32gui",
            target_name="MKWF-Helper.exe",
            shortcut_name="MKWF-Helper",
            shortcut_dir="DesktopFolder"
        )
    ],
)
