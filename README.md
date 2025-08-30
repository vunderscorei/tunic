![TUNIC Logo, which is the word TUNIC in grey](./resources/tunic_logo.png)

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

__HOW IT WORKS:__

In 2013, a "generous donor" donated a massive archive of Usenet newsgroups going as far back as the mid 1980s to the Internet Archive, who sorted through all of the data, and made it free for all to download in the MBOX format. While rarely used directly anymore, Mozilla Thunderbird still supports importing MBOX files as a mailbox through the use of the ImportExportTools NG plugin. This can handle most MBOX files without issue, but the ones hosted on the Internet Archive are slightly nonstandard, and appear to be an amalgamation of a number of different archives. This leads to a number of issues if the MBOX files are directly imported, most notably handling of dates. A number of the newsgroups have message dates in both the `YYYY/MM/dd` and `MM-dd-YYYY` formats in the same file, which ImportExportTools NG cannot handle (and for speed reasons, [likely never will](https://github.com/thunderbird/import-export-tools-ng/issues/524)).

As such, the job of TUNIC can be broken into four parts.
 - Read in a specific newsgroup from the user
 - Locate and download the associated MBOX via the [interentarchive](https://archive.org/developers/internetarchive/) python library
 - Convert all metadata dates to the `MM-dd-YYYY` format while careful not to modify any message bodies
 - Save the converted MBOX file to disk and alert the user the download has finished.

---

__FREQUENTLY ASKED QUESTIONS:__

*(Disclaimer: Nobody's ever actually asked these, TUNIC isn't popular enough to get questions. These are all made up.)*

- ***Why does macOS or Windows think TUNIC is a virus?***
    - In order to make the scary "unverified" or "may be a virus" screens to go away on modern operation systems, TUNIC would need to be notarized with a code signing tool from Apple and Microsoft. This is their assurance that they believe I'm a trustworthy developer. However, this process requires developer accounts that cost hundreds of dollars each, and must be tied to my legal name. I'd like to stay anonymous, so for now users will need to bypass the warnings if they want to run TUNIC.

- ***Why can't TUNIC automatically import newsgroups into Thunderbird?***
    - The plugin used for MBOX imports, ImportExportToolNG, does not provide a command line interface. Thunderbird does support GUI automation through [Puppeteer](https://pptr.dev/supported-browsers), but this is poorly documented, and would require users to click through even more warning popups to enable.

- ***Why is this a giant Python program? I could do that with a 2-line sed script!***
     - I agree, and if the command line doesn't scare you, [here's how](https://github.com/vunderscorei/tunic/wiki/Fixing-MBOXs-without-TUNIC) to do just that. TUNIC started as a tool written in `sed` before I discovered there was no good Windows built-in equivalent to handle hundreds of megabytes of text at a time. Additionally, the Internet Archive attempts to block most direct `curl` requests, and would strongly prefer you use their [python library](https://archive.org/developers/internetarchive/) for downloads, meaning any proper command line tool would already have to bring in python as a dependency.
 
- ***How complete are the Usenet archives used by TUNIC? Does it pull from Google Groups?***
    - Due to the exact way in which Usenet is distrubted, it is impossible to tell the exact number of posts that have been made, especially in the earlier years. TUNIC relies entirely upon the [Usenet Historical Collection](https://archive.org/details/usenethistorical), a massive dump given to the Internet Archive which does include anything newer than late 2013. It appears to go as far back as 1984 or 1985, but early archiving seems spotty. Google Groups, one of the only other large-scale historic Usenet archives, has a significanlty more posts from these early years, but are unfortunatley not used by TUNIC. The Usenet archive section of Google Groups has been languishing for more than a decade, and the API to interface with it is completely broken. There have been some attempts to scape posts from it, but those are beyond the scope of TUNIC, which has the goal of just reading wha has already been collected.

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
