from tkinter import ttk
import tkinter as tk

import tunicui
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

btn_download : ttk.Button = ttk.Button(root, text='Download', state=tk.DISABLED)

sv_status : tk.StringVar = tk.StringVar()

label_link : ttk.Label = tunicui.new_hyperlink(root, 'Made by vi', 'https://v-i.dev')

img_icon : tk.PhotoImage = tk.PhotoImage(file=util.get_resource('tunic_logo.png'))