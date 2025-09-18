from tkinter import filedialog, ttk
import tkinter as tk

import iatalker
import backend
from backend import IPAD_X, PAD_X, PAD_Y
from threading import Thread
import time
import util

root : tk.Tk = tk.Tk()

sv_newsgroup : tk.StringVar = tk.StringVar()
entry_newsgroup : ttk.Entry = ttk.Entry(root, textvariable=sv_newsgroup)

btn_verify : ttk.Button = ttk.Button(root, text='Verify')

sv_filepath : tk.StringVar = tk.StringVar()
entry_filepath : ttk.Entry = ttk.Entry(root, textvariable=sv_filepath)

btn_browse : ttk.Button = ttk.Button(root, text='Browse')

bv_fix_dates : tk.BooleanVar = tk.BooleanVar()
chk_fix_dates : ttk.Checkbutton = ttk.Checkbutton(root, text='Fix dates (recommended)', variable=bv_fix_dates, onvalue=True, offvalue=False)

sv_download : tk.StringVar = tk.StringVar()
btn_download : ttk.Button = ttk.Button(root, textvariable=sv_download, state=tk.DISABLED)

sv_status : tk.StringVar = tk.StringVar()

label_link : ttk.Label = backend.new_hyperlink(root, 'Made by vi', 'https://v-i.dev')

img_icon : tk.PhotoImage = tk.PhotoImage(file=util.get_resource('tunic_logo.png'))

is_downloading : bool = False
download : iatalker.FileDownload | None = None
# ---

def cb_allow_buttons(_read : str, _write : str, _unset : str) -> None:
    ng_size : int = len(sv_newsgroup.get())
    if ng_size > 0:
        btn_verify.configure(state=tk.ACTIVE)
    else:
        btn_verify.configure(state=tk.DISABLED)

    if ng_size > 0 and len(sv_filepath.get()) > 0:
        btn_download.configure(state=tk.ACTIVE)
    else:
        btn_download.configure(state=tk.DISABLED)


def cb_verify_group() -> None:
    group : str = sv_newsgroup.get()
    file_size : int = iatalker.get_size(group)
    if file_size > -1:
        sv_status.set('Verified %s on the Internet Archive (%s).' % (group, util.friendly_size(file_size)))
    else:
        sv_status.set('ERROR: Could not find newsgroup %s on the Internet Archive.' % group)


def cb_select_file() -> None:
    group : str = sv_newsgroup.get()
    default_name : str | None = '%s.mbox' % group if group else None
    filename : str = filedialog.asksaveasfilename(defaultextension='.mbox', filetypes=[('MBOX', '*.mbox'), ('All Files', '*.*')], initialfile=default_name)
    if filename:
        sv_filepath.set(filename)


def cb_download() -> None:
    global is_downloading
    global download
    if is_downloading:
        if download:
            download.stop_requested = True
            while not download.done:
                time.sleep(0.5)

        download = None
        btn_verify.configure(state=tk.ACTIVE)
        btn_download.configure(state=tk.ACTIVE)
        sv_download.set('Download')
        sv_status.set('Download cancelled.')
        is_downloading = False
    else:
        download =



root.wm_title('TUNIC: Thunderbird Usenet Newsgroup Import Converter')
root.wm_minsize(width=600, height=200)
# todo: menubar

ttk.Label(root, text='Newsgroup Name').grid(row=0, sticky=tk.E, pady=PAD_Y, padx=PAD_X)

sv_newsgroup.trace_add(mode='write', callback=cb_allow_buttons)
sv_newsgroup.set(value='rec.arts.anime')

entry_newsgroup.grid(row=0, column=1, ipadx=IPAD_X)

btn_verify.configure(command=cb_verify_group)
btn_verify.grid(row=0, column=2, sticky=tk.W, pady=PAD_Y)

ttk.Label(root, text='Output MBOX').grid(row=1, sticky=tk.E, pady=PAD_Y, padx=PAD_X)

sv_filepath.trace_add(mode='write', callback=cb_allow_buttons)

entry_filepath.grid(row=1, column=1, ipadx=IPAD_X)

btn_browse.configure(command=cb_select_file)
btn_browse.grid(row=1, column=2, sticky=tk.W, pady=PAD_Y)

chk_fix_dates.grid(row=2, columnspan=2, sticky=tk.W, pady=PAD_Y, padx=PAD_X)

btn_download.configure(command=cb_download)
btn_download.grid(row=3, column=1, pady=PAD_Y)

sv_status.set('')
ttk.Label(root, textvariable=sv_status).grid(row=4, columnspan=4)

label_link.grid(row=5, column=1)


def main() -> None:
    root.focus()
    root.mainloop()


if __name__ == '__main__':
    main()
