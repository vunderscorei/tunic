import enum
from enum import Enum
import math
import sys


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