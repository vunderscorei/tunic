import enum
import os.path
from enum import Enum
import math
from os import path
from pathlib import Path
import sys

VERSION_NUM = '0.0.1.0'
PROJECT_ROOT = Path(path.dirname(path.dirname(path.realpath(__file__))))


def friendly_size(size_bytes : int) -> str:
    if size_bytes == 0:
        return '0 B'
    sizes : tuple[str, str, str, str, str] = ('B', 'KiB', 'MiB', 'GiB', 'TiB')
    index : int = int(math.floor(math.log(size_bytes, 1_024)))
    prefix : str = round(size_bytes / (1_204 ** index), 2)
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


def get_resource(name) -> Path:
    if get_os() == OS.MAC and (PROJECT_ROOT / 'Resources' / 'resources').exists():
        return PROJECT_ROOT / 'Resources' / 'resources' / name
    else:
        return PROJECT_ROOT / 'resources' / name
