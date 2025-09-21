import os.path
import tkinter as tk
from collections.abc import Callable
from io import BytesIO
from threading import Thread
from tkinter import filedialog, ttk
from zipfile import ZipFile

import iatalker
import util


def build_cb_verify_group(group_var: tk.StringVar, log_var: tk.StringVar) -> None:
    group: str = group_var.get()
    file_size: int = iatalker.get_size(group)
    if file_size > -1:
        log_var.set('Verified %s on the Internet Archive (%s).' % (group, util.friendly_size(file_size)))
    else:
        log_var.set('ERROR: Could not find newsgroup %s on the Internet Archive.' % group)


def build_cb_select_file(group_var: tk.StringVar, filepath_var: tk.StringVar) -> None:
    group: str = group_var.get()
    default_name: str | None = '%s.mbox' % group if group else None
    filename: str = filedialog.asksaveasfilename(defaultextension='.mbox',
                                                 filetypes=[('MBOX', '*.mbox'), ('All Files', '*.*')],
                                                 initialfile=default_name)
    if filename:
        filepath_var.set(filename)


# StringVar traces require a very specific type of callback
def build_cb_allow_buttons(group_var: tk.StringVar, filepath_var: tk.StringVar, verify: ttk.Button,
                           download: ttk.Button) -> Callable[[str, str, str], None]:
    def cb_allow_buttons(_read: str, _write: str, _unset: str) -> None:
        ng_size: int = len(group_var.get())
        if ng_size > 0:
            verify.configure(state=tk.ACTIVE)
            if len(filepath_var.get()) > 0:
                download.configure(state=tk.ACTIVE)
            else:
                download.configure(state=tk.DISABLED)
        else:
            verify.configure(state=tk.DISABLED)

    return cb_allow_buttons


def _async_get_mbox(group_var: tk.StringVar, filepath_var: tk.StringVar, log_var: tk.StringVar, fix_flag: tk.BooleanVar,
                    cancel_flag: tk.BooleanVar, callback: Callable[[], None] | None = None) -> None:
    log_var.set('Downloading...')
    group: str = group_var.get()
    try:
        group_size: int = iatalker.get_size(group)
        if group_size == -1:
            log_var.set('ERROR: Could not find newsgroup %s on the Internet Archive.' % group)
            return callback() if callback else None

        if cancel_flag.get():
            log_var.set('Download cancelled')
            return callback() if callback else None

        url: str = iatalker.get_url(group_var.get())
        data: BytesIO | None = iatalker.download(url=url, target_size=group_size, cancel_flag=cancel_flag,
                                                 log_var=log_var)

        if cancel_flag.get():
            log_var.set('Download cancelled')
            return callback() if callback else None
        elif not data:
            log_var.set('Could not download newsgroup')
            return callback() if callback else None
    except Exception as e:
        log_var.set('ERROR: %s' % e)
        return callback() if callback else None

    log_var.set('Decompressing...')
    filepath: str = filepath_var.get()
    with ZipFile(data) as z:
        mbox: str = z.read(group + '.mbox').decode(encoding='utf-8')
        with open(filepath, 'w', encoding='utf-8') as file:
            if fix_flag.get():
                log_var.set('Fixing...')
                file.write(util.fix_mbox(mbox))
            else:
                file.write(mbox)

    if cancel_flag.get():
        if os.path.exists(filepath):
            os.remove(filepath)
        log_var.set('Download cancelled')
        return callback() if callback else None

    log_var.set('Done.')
    return callback() if callback else None


def build_cb_download(group_var: tk.StringVar, filepath_var: tk.StringVar, log_var: tk.StringVar,
                      fix_flag: tk.BooleanVar, cancel_flag: tk.BooleanVar, download_btn_text_var: tk.StringVar,
                      disable_while_dl: list[ttk.Button | ttk.Entry | ttk.Checkbutton] | None) -> None:
    if download_btn_text_var.get() == 'Download':
        def cb_download_cb() -> None:
            if disable_while_dl:
                for i in disable_while_dl:
                    i.configure(state=tk.ACTIVE)
            download_btn_text_var.set('Download')
            cancel_flag.set(False)

        if disable_while_dl:
            for item in disable_while_dl:
                item.configure(state=tk.DISABLED)

        download_btn_text_var.set('Cancel')

        Thread(target=lambda: _async_get_mbox(group_var=group_var, filepath_var=filepath_var, log_var=log_var,
                                              fix_flag=fix_flag, cancel_flag=cancel_flag,
                                              callback=cb_download_cb)).start()
    else:  # cancel
        cancel_flag.set(True)
