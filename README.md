__TUNIC: The Thunderbird Usenet Newsgroup Import Converter__

A cross-platform tool for downloading and converting Usenet MBOX files from the Internet Archive into something that can be read by Thunderbird.

Currently in development and not really ready for use.

[__CLICK HERE TO DOWNLOAD__](https://github.com/vunderscorei/tunic/releases)

---

__BUILDING:__

Requirements:
- Python 3.13 or greater
- macOS, Windows, or Linux *(note: ***not tested*** on Linux)*
  - Building on macOS will produce universal x64/ARM binaries, but building on other platforms will only compile for a single target architecture.

Process:
- Clone the repository with `git clone https://github.com/vunderscorei/tunic.git`
- Navigate to the project directory and run `pip install -r requirements.txt` to download the project dependencies.
- Run `python scripts/build.py` (or `python scripts\build.py` on Windows) to compile the project using pyinstaller.
- The compiled executable will be in the `dist` directory. On Windows, this will be a folder called `TUNIC`, on macOS, a single file called `TUNIC.app`, and on Linux, a single file called `TUNIC`.

---

__KNOWN ISSUES:__
- Light/Dark mode detect doesn't work correctly on Windows.
- Many UI elements are unreadable in dark mode on macOS.
- The program provides no feedback if a download crashes, and will appear to be downloading forever.
- The "finished" text can sometimes get garbled when it appears on Windows.
- The app icon is awful.
- Occasionally quitting the app on Windows leads to a zombie background task.
- The entire UI is off-center and really ugly.
- The tray icon on Windows is still a placeholder feather icon.
- The menu bar on macOS is still filled with TkInter placeholder options.
- No instructions on how to actually import the downloaded MBOX files into Thunderbird have been prepared.
- Zero testing has been done on Linux.
