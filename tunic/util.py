import enum
import math
import re
import sys
import tkinter as tk
import webbrowser
from enum import Enum
from os import path
from pathlib import Path
from tkinter import font, ttk

VERSION_NUM: str = '0.1.0.0'
HOMEPAGE = 'https://github.com/vunderscorei/tunic'
PROJECT_ROOT: Path = Path(path.dirname(path.dirname(path.realpath(__file__))))

RESOURCE_ROOT = PROJECT_ROOT / 'TUNIC' / 'resources'
RESOURCE_ROOT_MAC = PROJECT_ROOT / 'Resources' / 'resources'
RESOURCE_ROOT_LOOSE = PROJECT_ROOT / 'resources'


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


def friendly_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return '0 B'
    sizes: tuple[str, str, str, str, str] = ('B', 'KiB', 'MiB', 'GiB', 'TiB')
    index: int = int(math.floor(math.log(size_bytes, 1_024)))
    prefix: str = round(size_bytes / (1_024 ** index), 2)
    return '%s %s' % (prefix, sizes[index])


def get_resource(name: str) -> Path:
    # this is slow, but allows macOS to work both bundled and as a folder of random files
    if get_os() == OS.MAC:
        if (RESOURCE_ROOT_MAC / name).exists():
            return RESOURCE_ROOT_MAC / name
        else:
            return RESOURCE_ROOT_LOOSE / name
    else:
        if (RESOURCE_ROOT / name).exists():
            return RESOURCE_ROOT / name
        else:
            return RESOURCE_ROOT_LOOSE / name


def fix_mbox(data: str) -> str:
    return re.sub(r'\nDate: ([0-9]{4})/([0-9]{2})/([0-9]{2})\n', r'\nDate: \2-\3-\1\n', data)


def set_underline(label: ttk.Label, underline: bool = True) -> None:
    lbl_font: font.Font = font.Font(label, label.cget('font'))
    lbl_font.configure(underline=underline)
    label.configure(font=lbl_font)


def new_hyperlink(root: tk.Tk | tk.Toplevel, text: str, url: str) -> ttk.Label:
    label: ttk.Label = ttk.Label(master=root, text=text, foreground='blue', cursor='hand2')
    set_underline(label=label, underline=True)
    label.bind('<Button-1>', lambda _: webbrowser.open_new_tab(url))
    return label
