import enum
from enum import Enum
import math
from os import path
from pathlib import Path
import re
import sys

VERSION_NUM : str = '0.0.1.0'
PROJECT_ROOT : Path = Path(path.dirname(path.dirname(path.realpath(__file__))))

def friendly_size(size_bytes : int) -> str:
    if size_bytes == 0:
        return '0 B'
    sizes : tuple[str, str, str, str, str] = ('B', 'KiB', 'MiB', 'GiB', 'TiB')
    index : int = int(math.floor(math.log(size_bytes, 1_024)))
    prefix : str = round(size_bytes / (1_024 ** index), 2)
    return '%s %s' % (prefix, sizes[index])


class OS(Enum):
    LINUX = enum.auto()
    MAC = enum.auto()
    WINDOWS = enum.auto()


def get_os() -> OS:
    match sys.platform:
        case 'linux':
            return OS.LINUX
        case 'darwin':
            return OS.MAC
        case _:
            return OS.WINDOWS


def get_resource(name : str) -> Path:
    # this is slow, but allows macOS to work both bundled and as a folder of random files
    if get_os() == OS.MAC and (PROJECT_ROOT / 'Resources' / 'resources').exists():
        return PROJECT_ROOT / 'Resources' / 'resources' / name
    else:
        return PROJECT_ROOT / 'resources' / name


def fix_mbox(data : str) -> str:
    return re.sub(r'\nDate: ([0-9]{4})/([0-9]{2})/([0-9]{2})\n', r'\nDate: \2-\3-\1\n', data)

