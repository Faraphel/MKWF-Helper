import os
from pathlib import Path

from source import CACHE_PATH, TOOLS_PATH
from source.wt import get_call_tools


call_tools = get_call_tools(TOOLS_PATH / "wit/wit")


def extract_subfile(path: Path, subpath: str) -> Path:
    process = call_tools(
        "EXTRACT", path,
        f"--files", f"+{subpath}",
        "--DEST", CACHE_PATH,
        "--flat",
        "--overwrite"
    )

    if process.returncode != 0:
        raise Exception("Can't extract the file.")

    return Path(CACHE_PATH / os.path.basename(subpath))
