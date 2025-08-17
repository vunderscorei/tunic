import enum
from enum import Enum
from os import path
from pathlib import Path
import PyInstaller.__main__
import sys

PROJECT_ROOT = Path(path.dirname(path.dirname(path.realpath(__file__))))

PY_FILES = (
    'tunicui.py',
    'theme.py',
    'iatalker.py'
)

ICON = PROJECT_ROOT / 'resources' / 'tunic_logo.ico'
ICON_MAC = PROJECT_ROOT / 'resources' / 'tunic_logo.icns'


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


def pyinstall(args : list[str]) -> None:
    PyInstaller.__main__.run(args)


def main():
    os : OS = get_os()
    args : list[str] = []
    for py in PY_FILES:
        args.append(str(PROJECT_ROOT / 'tunic' / py))
    args.append('--distpath')
    args.append(str(PROJECT_ROOT / 'dist'))
    args.append('--specpath')
    args.append(str(PROJECT_ROOT / 'dist' / 'spec'))
    args.append('--workpath')
    args.append(str(PROJECT_ROOT / 'build'))
    args.append('--noconfirm')
    args.append('--clean')
    args.append('--name')
    args.append('TUNIC')
    if os == OS.MAC:
        args.append('--icon')
        args.append(str(ICON_MAC))
        args.append('--windowed')
        args.append('--osx-bundle-identifier')
        args.append('dev.v-i.tunic')
        args.append('--target-architecture')
        args.append('universal2')
    else:
        args.append('--icon')
        args.append(str(ICON))
        args.append('--onefile')

    pyinstall(args)

if __name__ == '__main__':
    main()