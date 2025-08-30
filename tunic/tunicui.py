from collections.abc import Callable
import internetarchive as ia
import math
import re
from threading import Thread
from tkinter import filedialog, font, ttk
import tkinter as tk
import webbrowser
from zipfile import ZipFile

import iatalker
from theme import theme


def friendly_size(size_bytes : int) -> str:
    if size_bytes == 0:
        return '0 B'
    sizes : tuple[str, str, str, str, str] = ('B', 'KiB', 'MiB', 'GiB', 'TiB')
    index : int = int(math.floor(math.log(size_bytes, 1_024)))
    prefix : str = round(size_bytes / (1_204 ** index), 2)
    return '%s %s' % (prefix, sizes[index])


def fix_mbox(data : str) -> str:
    return re.sub(r'\nDate: ([0-9]{4})/([0-9]{2})/([0-9]{2})\n', r'\nDate: \2-\3-\1\n', data)


def new_hyperlink(root_window : tk.Tk, text: str, url : str) -> ttk.Label:
    label : ttk.Label = ttk.Label(master=root_window, text=text, foreground=theme.hyperlink, cursor='hand2')
    ul_font : font.Font = font.Font(label, label.cget('font'))
    ul_font.configure(underline=True)
    label.configure(font=ul_font)
    label.bind('<Button-1>', lambda _: webbrowser.open_new_tab(url))
    return label


def get_mbox(group : str, filepath : str, fix : Callable[[str], str] | None = None, progress_print : tk.StringVar | None = None) -> bool:
    if len(filepath) == 0:
        return False
    file_ref : ia.File = iatalker.get_file_ref(group)
    if not file_ref:
        return False
    fdl : iatalker.FileDownload = iatalker.FileDownload(file_ref)
    fdl.download_async()
    while not fdl.done:
        if progress_print:
            percent = int(fdl.progress() * 100.0)
            progress_print.set('Downloading... (%d%%)' % percent)
    if progress_print:
        progress_print.set('Decompressing...')
    with ZipFile(fdl) as z:
        data : str = z.read(group + '.mbox').decode(encoding='utf-8')
        with open(filepath, 'w', encoding='utf-8') as mbox:
            if fix:
                if progress_print:
                    progress_print.set('Fixing...')
                mbox.write(fix(data))
            else:
                mbox.write(data)

            if progress_print:
                progress_print.set('Done.')
            return True


root : tk.Tk = tk.Tk()

sv_newsgroup : tk.StringVar = tk.StringVar()
entry_newsgroup : ttk.Entry = ttk.Entry(root, textvariable=sv_newsgroup)

button_verify : ttk.Button = ttk.Button(root, text='Verify')

sv_filepath : tk.StringVar = tk.StringVar()
entry_filepath : ttk.Entry = ttk.Entry(root, textvariable=sv_filepath)

button_filepick : ttk.Button = ttk.Button(root, text='Browse')

button_download : ttk.Button = ttk.Button(root, text='Download', state=tk.DISABLED)

sv_status : tk.StringVar = tk.StringVar()

label_link : ttk.Label = new_hyperlink(root, 'Made by vi', 'https://v-i.dev')


def cb_allow_buttons(_read : str, _write : str, _unset : str) -> None:
    ng_size : int = len(sv_newsgroup.get())
    if ng_size > 0:
        button_verify.configure(state=tk.ACTIVE)
    else:
        button_verify.configure(state=tk.DISABLED)

    if ng_size > 0 and len(sv_filepath.get()) > 0:
        button_download.configure(state=tk.ACTIVE)
    else:
        button_download.configure(state=tk.DISABLED)


def cb_verify_group() -> None:
    group : str = sv_newsgroup.get()
    file_ref : ia.File = iatalker.get_file_ref(group)
    if file_ref:
        sv_status.set('Verified %s on the Internet Archive (%s).' % (group, friendly_size(int(file_ref.metadata['size']))))
    else:
        sv_status.set('Could not find newsgroup %s on the Internet Archive.' % group)


def cb_select_file() -> None:
    group : str = sv_newsgroup.get()
    default_name : str | None = '%s.mbox' % group if group else None
    filename : str = filedialog.asksaveasfilename(defaultextension='.mbox', filetypes=[('MBOX', '*.mbox'), ('All Files', '*.*')], initialfile=default_name)
    if filename:
        sv_filepath.set(filename)


def t_download() -> None:
    newsgroup : str = sv_newsgroup.get()
    filepath : str = sv_filepath.get()
    button_verify.configure(state=tk.DISABLED)
    button_download.configure(state=tk.DISABLED)
    if not get_mbox(group=newsgroup, filepath=filepath, fix=fix_mbox, progress_print=sv_status):
        sv_status.set('An error has occurred.')
    button_verify.configure(state=tk.ACTIVE)
    button_download.configure(state=tk.ACTIVE)


def cb_download() -> None:
    Thread(target=t_download).start()



root.wm_title('TUNUC: Thunderbird Usenet Newsgroup Import Converter')
root.wm_minsize(width=600, height=200)

ttk.Label(root, text='Newsgroup Name').grid(row=0, sticky=tk.E, pady=4)

#BEDUG
print(ttk.Style(root).configure('lightcolor'))

sv_newsgroup.trace_add(mode='write', callback=cb_allow_buttons)
sv_newsgroup.set('rec.arts.anime')

entry_newsgroup.grid(row=0, column=1, ipadx=75)

button_verify.configure(command=cb_verify_group)
button_verify.grid(row=0, column=2, sticky=tk.W, pady=4)

ttk.Label(root, text='Output MBOX').grid(row=1, sticky=tk.E, pady=4)

sv_filepath.trace_add(mode='write', callback=cb_allow_buttons)

entry_filepath.grid(row=1, column=1, ipadx=75)

button_filepick.configure(command=cb_select_file)
button_filepick.grid(row=1, column=2, sticky=tk.W, pady=4)

button_download.configure(command=cb_download)
button_download.grid(row=2, column=1, pady=4)

sv_status.set('')
ttk.Label(root, textvariable=sv_status).grid(row=3, columnspan=4)

label_link.grid(row=4, column=1)


def main() -> None:
    root.focus()
    root.mainloop()


if __name__ == '__main__':
    main()