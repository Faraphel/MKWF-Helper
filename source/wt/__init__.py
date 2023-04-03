import subprocess
from pathlib import Path


def get_call_tools(tools_path: Path):
    def wrapper(*args) -> subprocess.CompletedProcess:
        return subprocess.run([tools_path, *args], stdout=subprocess.PIPE)

    return wrapper
