from collections.abc import Callable
from io import BytesIO
from threading import Thread
import json
from tkinter import filedialog, font, ttk
import tkinter as tk
from urllib import request
import webbrowser
from zipfile import ZipFile

import iatalker
import util

PAD_Y : int | tuple[int, int] = 4
PAD_X : int | tuple[int, int] = (10, 0)
IPAD_X : int = 75

def set_underline(label : ttk.Label, underline : bool = True):
    lbl_font : font.Font = font.Font(label, label.cget('font'))
    lbl_font.configure(underline=underline)
    label.configure(font=lbl_font)


def new_hyperlink(root : tk.Tk | tk.Toplevel, text : str, url : str) -> ttk.Label:
    label : ttk.Label = ttk.Label(master=root, text=text, foreground='blue', cursor='hand2')
    set_underline(label=label, underline=True)
    label.bind('<Button-1>', lambda _: webbrowser.open_new_tab(url))
    return label


def get_size(newsgroup : str) -> int:
    root : str = newsgroup.split('.')[0]
    meta_url : str = 'https://archive.org/metadata/usenet-%s/files/%s.mbox.zip' % (root, newsgroup)
    with request.urlopen(meta_url) as resp:
        body : dict = json.loads(resp.read())
    if body and 'result' in body:
        return int(body['result']['size'])
    else:
        return -1


def get_url(newsgroup : str) -> str:
    root : str = newsgroup.split('.')[0]
    return 'https://archive.org/download/usenet-%s/%s.mbox.zip' % (root, newsgroup)


class MboxDownload(BytesIO):

    def __init__(self, group : str, filepath : str, progress_print : tk.StringVar, fix : bool, chunk_size : int = 1_000_000) -> None:
        super().__init__()
        self.group : str = group
        self.filepath : str = filepath
        self.progress_print : tk.StringVar = progress_print
        self.fix : bool = fix
        self.chunk_size : int = chunk_size
        self._current_size : int = 0
        self._done : bool = False
        self._success : bool = False
        self._stop_requested : bool = False
        self.thread : Thread | None = None


    def _download(self) -> bool:
        if len(self.group) == 0:
            self.progress_print.set('ERROR: No newsgroup given.')
            if self.after:
                self.after()
            return False
        elif len(self.filepath) == 0:
            self.progress_print.set('ERROR: No filepath given.')
            if self.after:
                self.after()
            return False

        size : int = iatalker.get_size(self.group)
        if size == -1:
            self.progress_print.set('ERROR: Could not find newsgroup %s on the Internet Archive.' % self.group)
            if self.after:
                self.after()
            return False

        mbox_url : str = iatalker.get_url(self.group)
        with request.urlopen(mbox_url) as resp:
            while True:
                if self._stop_requested:
                    self._done = True
                    if self.after:
                        self.after()
                    return False

                buffer : bytes | None = resp.read(self.chunk_size)
                if not buffer:
                    break
                self.write(buffer)
                self._current_size += len(buffer)
                self.progress_print.set('Downloading... (%d%%)' % (self._current_size * 100.0))
            self.progress_print.set('Decompressing...')

            with ZipFile(self) as z:
                data : str = z.read(self.group + '.mbox').decode(encoding='utf-8')
                with open(self.filepath, 'w', encoding='utf-8') as mbox:
                    if self.fix:
                        self.progress_print.set('Fixing...')
                        mbox.write(util.fix_mbox(data))
                    else:
                        mbox.write(data)
                self.progress_print.set('Done.')
                self._done = True
                self._success = True
                if self.after:
                    self.after()
                return True

    def download_async(self) -> Thread:
        self.thread = Thread(target=self._download)
        self.thread.start()
        return self.thread

    def join(self, timeout : float | None = None) -> None:
        if self.thread:
            self.thread.join(timeout=timeout)

    def stop(self) -> Thread | None:
        self._stop_requested = True
        return self.thread

    def is_done(self) -> bool:
        return self._done

    def is_success(self) -> bool:
        return self._success



def download_mbox(group : str, filepath : str,  progress_print : tk.StringVar, fix : Callable[[str], str] | None = None) -> bool:
    if len(group) == 0:
        progress_print.set('ERROR: No newsgroup given.')
        return False
    elif len(filepath) == 0:
        progress_print.set('ERROR: No filepath given.')
        return False

    size = iatalker.get_size(group)
    if size == -1:
        progress_print.set('ERROR: Could not find newsgroup %s on the Internet Archive.' % group)

    mbox_url : str = iatalker.get_url(group)
    fdl : iatalker.FileDownload = iatalker.FileDownload(url=mbox_url, target_size=size)
    fdl.download_async()
    while not fdl.done:
        percent = int(fdl.progress() * 100.0)
        progress_print.set('Downloading... (%d%%)' % percent)

    progress_print.set('Decompressing...')

    with ZipFile(fdl) as z:
        data : str = z.read(group + '.mbox').decode(encoding='utf-8')
        with open(filepath, 'w', encoding='utf-8') as mbox:
            if fix:
                progress_print.set('Fixing...')
                mbox.write(fix(data))
            else:
                mbox.write(data)

            progress_print.set('Done.')
            return True
