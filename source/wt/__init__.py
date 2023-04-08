import subprocess
from pathlib import Path


def get_call_tools(tools_path: Path):
    def wrapper(*args) -> subprocess.CompletedProcess:
        return subprocess.run(
            [tools_path, *args],
            stdout=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    return wrapper
