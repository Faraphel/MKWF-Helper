from pathlib import Path

from source import TOOLS_PATH
from source.wt import get_call_tools


call_tools = get_call_tools(TOOLS_PATH / "szs/wszst")


def sha1(path: Path) -> str:
    return call_tools("SHA1", path).stdout.decode().split(" ")[0]
