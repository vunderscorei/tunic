from os import path
from pathlib import Path
import PyInstaller.__main__

from tunic import util

VERSION = [ '1', '0', '0', '0']

PROJECT_ROOT = Path(path.dirname(path.dirname(path.realpath(__file__))))

PY_FILES = (
    'util.py',
    'tunicui.py',
    'theme.py',
    'iatalker.py'
)

ICON = PROJECT_ROOT / 'resources' / 'tunic_logo.ico'
ICON_MAC = PROJECT_ROOT / 'resources' / 'tunic_logo.icns'
FFI_TEMPLATE = PROJECT_ROOT / 'scripts' / 'windows_ver.ffi.template'
FFI_OUT = PROJECT_ROOT / 'dist' / 'spec' / 'windows_ver.ffi'


def pyinstall(args : list[str]) -> None:
    PyInstaller.__main__.run(args)


def make_ffi() -> None:
    with open(FFI_TEMPLATE, 'r') as template:
        text = template.read().format(
            DATE='0',
            TIMESTAMP='0',
            FILE_VER1=VERSION[0],
            FILE_VER2=VERSION[1],
            FILE_VER3=VERSION[2],
            FILE_VER4=VERSION[3]
        )
        with open(FFI_OUT, 'w') as outfile:
            outfile.write(text)


def main():
    os : util.OS = util.get_os()
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
    args.append('--windowed')
    if os == util.OS.MAC:
        args.append('--icon')
        args.append(str(ICON_MAC))
        args.append('--osx-bundle-identifier')
        args.append('dev.v-i.tunic')
        args.append('--target-architecture')
        args.append('universal2')
    else:
        if os == util.OS.LINUX:
            # causes program to be marked as a virus on windows, linux only for now
            args.append('--one-file')
        elif os == util.OS.WINDOWS:
            make_ffi()
            args.append('--version-file')
            args.append(str(FFI_OUT))

        args.append('--icon')
        args.append(str(ICON))
    pyinstall(args)

if __name__ == '__main__':
    main()