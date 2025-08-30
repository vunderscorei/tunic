import enum
from enum import Enum
from os import path
from pathlib import Path
import PyInstaller.__main__
import sys

PROJECT_ROOT = Path(path.dirname(path.dirname(path.realpath(__file__))))

VERSION : (str, str, str, str) = ('1', '0', '0', '0')
VERSION_STR : str = '.'.join(VERSION)

PY_FILES : list[str] = [
    str(PROJECT_ROOT / 'tunic' / 'tunicui.py'),
    str(PROJECT_ROOT / 'tunic' / 'iatalker.py'),
    str(PROJECT_ROOT / 'tunic' / 'theme.py'),
    str(PROJECT_ROOT / 'tunic' / 'util.py')
]

ICON = PROJECT_ROOT / 'resources' / 'tunic_logo.ico'
ICON_MAC = PROJECT_ROOT / 'resources' / 'tunic_logo.icns'

SPEC_FILE = PROJECT_ROOT / 'scripts' / 'tunic.spec'


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
    pyinstall(args=[
        '--distpath',
        str(PROJECT_ROOT / 'dist'),
        '--workpath',
        str(PROJECT_ROOT / 'build'),
        '--noconfirm',
        '--clean',
        str(SPEC_FILE)
    ])


if __name__ == '__main__':
    main()