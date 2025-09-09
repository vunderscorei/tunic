from collections.abc import Callable
from io import BytesIO
from tkinter import filedialog, font, ttk
import tkinter as tk
import webbrowser
from zipfile import ZipFile

import iatalker
import util

def set_underline(label : ttk.Label, underline : bool = True):
    lbl_font : font.Font = font.Font(label, label.cget('font'))
    lbl_font.configure(underline=underline)
    label.configure(font=lbl_font)


def new_hyperlink(root : tk.Tk | tk.Toplevel, text : str, url : str) -> ttk.Label:
    label : ttk.Label = ttk.Label(master=root, text=text, foreground='blue', cursor='hand2')
    set_underline(label=label, underline=True)
    label.bind('<Button-1>', lambda _: webbrowser.open_new_tab(url))
    return label


def cb_verify_group(sv_newsgroup : tk.StringVar, sv_status : tk.StringVar) -> None:
    group : str = sv_newsgroup.get()
    file_size : int = iatalker.get_size(group)
    if file_size > -1:
        sv_status.set('Verified %s on the Internet Archive (%s).' % (group, util.friendly_size(file_size)))
    else:
        sv_status.set('ERROR: Could not find newsgroup %s on the Internet Archive.' % group)


def cb_select_file(sv_newsgroup : tk.StringVar, sv_filepath : tk.StringVar) -> None:
    group : str = sv_newsgroup.get()
    default_name : str | None = '%s.mbox' % group if group else None
    filename : str = filedialog.asksaveasfilename(defaultextension='.mbox', filetypes=[('MBOX', '*.mbox'), ('All Files', '*.*')], initialfile=default_name)
    if filename:
        sv_filepath.set(filename)


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