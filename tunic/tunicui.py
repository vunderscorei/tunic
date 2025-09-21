import tkinter as tk
import webbrowser
from collections.abc import Callable
from tkinter import ttk

import backend
import util

# constants
PAD_X: int | tuple[int, int] = (10, 0)
PAD_Y: int | tuple[int, int] = 4
IPAD_X: int = 75

# constructors
root: tk.Tk = tk.Tk()

sv_newsgroup: tk.StringVar = tk.StringVar()
entry_newsgroup: ttk.Entry = ttk.Entry(root, textvariable=sv_newsgroup)

btn_verify: ttk.Button = ttk.Button(root, text='Verify')

sv_filepath: tk.StringVar = tk.StringVar()
entry_filepath: ttk.Entry = ttk.Entry(root, textvariable=sv_filepath)

btn_browse: ttk.Button = ttk.Button(root, text='Browse')

bv_fix_dates: tk.BooleanVar = tk.BooleanVar()
chk_fix_dates: ttk.Checkbutton = ttk.Checkbutton(root, text='Fix dates (recommended)', variable=bv_fix_dates,
                                                 onvalue=True, offvalue=False)

sv_download: tk.StringVar = tk.StringVar()
btn_download: ttk.Button = ttk.Button(root, textvariable=sv_download)

sv_log: tk.StringVar = tk.StringVar()

label_link: ttk.Label = util.new_hyperlink(root, 'Made by vi', 'https://v-i.dev')

img_icon: tk.PhotoImage = tk.PhotoImage(file=util.get_resource('tunic_logo.png'))

bv_cancel: tk.BooleanVar = tk.BooleanVar()
bv_cancel.set(False)

# callbacks
cb_allow_buttons: Callable[[str, str, str], None] = backend.build_cb_allow_buttons(group_var=sv_newsgroup,
                                                                                   filepath_var=sv_filepath,
                                                                                   verify=btn_verify,
                                                                                   download=btn_download)

cb_verify_group: Callable[[], None] = lambda: backend.build_cb_verify_group(group_var=sv_newsgroup, log_var=sv_log)

cb_select_file: Callable[[], None] = lambda: backend.build_cb_select_file(group_var=sv_newsgroup,
                                                                          filepath_var=sv_filepath)

cb_download: Callable[[], None] = lambda: backend.build_cb_download(group_var=sv_newsgroup, filepath_var=sv_filepath,
                                                                    log_var=sv_log, fix_flag=bv_fix_dates,
                                                                    cancel_flag=bv_cancel,
                                                                    download_btn_text_var=sv_download,
                                                                    disable_while_dl=[btn_verify, btn_browse,
                                                                                      chk_fix_dates])

# placement
if util.get_os != util.OS.MAC:
    root.iconbitmap(util.get_resource('tunic_logo.ico'))

root.wm_title('TUNIC: Thunderbird Usenet Newsgroup Import Converter')
root.wm_minsize(width=600, height=200)

ttk.Label(root, text='Newsgroup Name').grid(row=0, column=0, sticky=tk.E, pady=PAD_Y, padx=PAD_X)

sv_newsgroup.trace_add(mode='write', callback=cb_allow_buttons)
sv_newsgroup.set(value='rec.arts.anime')

entry_newsgroup.grid(row=0, column=1, ipadx=IPAD_X)

btn_verify.configure(command=cb_verify_group)
btn_verify.grid(row=0, column=2, sticky=tk.W, pady=PAD_Y)

ttk.Label(root, text='Output MBOX').grid(row=1, column=0, sticky=tk.E, pady=PAD_Y, padx=PAD_X)

sv_filepath.trace_add(mode='write', callback=cb_allow_buttons)

entry_filepath.grid(row=1, column=1, ipadx=IPAD_X)

btn_browse.configure(command=cb_select_file)
btn_browse.grid(row=1, column=2, sticky=tk.W, pady=PAD_Y)

bv_fix_dates.set(True)
chk_fix_dates.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=PAD_Y, padx=PAD_X)

sv_download.set('Download')
btn_download.configure(state=tk.DISABLED)

btn_download.configure(command=cb_download)
btn_download.grid(row=3, column=1, pady=PAD_Y)

sv_log.set('')
ttk.Label(root, textvariable=sv_log).grid(row=4, column=0, columnspan=4)

label_link.grid(row=5, column=1)


# Menus
def cb_aboutbox() -> None:
    about: tk.Toplevel = tk.Toplevel(root)
    about.title('About TUNIC')
    about.geometry('250x200')
    ttk.Label(about, image=img_icon).pack(pady=10)
    ttk.Label(about, text='TUNIC v' + util.VERSION_NUM).pack(pady=10)
    util.new_hyperlink(root=about, text='Home Page', url=util.HOMEPAGE).pack(pady=10)


def cb_help() -> None:
    webbrowser.open_new_tab(util.HOMEPAGE)


menu_root: tk.Menu = tk.Menu(root)

menu_file: tk.Menu = tk.Menu(menu_root, tearoff=0)
menu_help: tk.Menu = tk.Menu(menu_root, tearoff=0)
if util.get_os() == util.OS.MAC:
    root.createcommand('tkAboutDialog', cb_aboutbox)
    menu_file.add_command(label='Verify', command=cb_verify_group, accelerator='Cmd+Y')
    root.bind_all('<Command-y>', lambda _: cb_verify_group())
    menu_file.add_command(label='Output as...', command=cb_select_file, accelerator='Cmd+S')
    root.bind_all('<Command-s>', lambda _: cb_select_file())
    menu_file.add_command(label='Start Download', command=cb_download, accelerator='Cmd+D')
    root.bind_all('<Command-d>', lambda _: cb_download())

    menu_help.add_command(label='Documentation...', command=cb_help, accelerator='Cmd+Shift+H')
    root.bind_all('<Command-H>', lambda _: cb_help())
else:
    menu_file.add_command(label='Verify', command=cb_verify_group, accelerator='Ctrl+Y')
    root.bind_all('<Control-y>', lambda _: cb_verify_group())
    menu_file.add_command(label='Output as...', command=cb_select_file, accelerator='Ctrl+S')
    root.bind_all('<Control-s>', lambda _: cb_select_file())
    menu_file.add_command(label='Start Download', command=cb_download, accelerator='Ctrl+D')
    root.bind_all('<Control-d>', lambda _: cb_download())
    menu_file.add_separator()
    menu_file.add_command(label='Exit', command=lambda: exit(), accelerator='Ctrl+Q')
    root.bind_all('<Control-q>', lambda _: exit())

    menu_help.add_command(label='About TUNIC', command=cb_aboutbox)
    menu_help.add_separator()
    menu_help.add_command(label='Documentation...', command=cb_help,
                          accelerator='F1')
    root.bind_all('<F1>', lambda _: cb_help())
menu_root.add_cascade(label='File', menu=menu_file)
menu_root.add_cascade(label='Help', menu=menu_help)
root.config(menu=menu_root)


def main() -> None:
    root.focus_force()
    root.mainloop()


if __name__ == '__main__':
    main()
