# -*- mode: python -*-

from PyInstaller.building.api import EXE, COLLECT, PYZ
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.osx import BUNDLE  # ignore any IDE warnings here

import build
from build import OS

extra_files = [
    (build.ICON, 'resources/'),
    (build.ICON_PNG, 'resources/')
]

platform: OS = build.get_os()
if platform == OS.LINUX:
    icon = build.ICON
    version = build.VERSION_STR
elif platform == OS.MAC:
    icon = build.ICON_MAC
    version = None  # set later via PLIST
else:  # windows
    from PyInstaller.utils.win32.versioninfo import (
        VSVersionInfo,
        FixedFileInfo,
        StringFileInfo,
        StringTable,
        StringStruct,
        VarFileInfo,
        VarStruct
    )

    icon = build.ICON
    version = VSVersionInfo(
        ffi=FixedFileInfo(
            filevers=build.VERSION,
            prodvers=build.VERSION,
            mask=0x3F,
            flags=0x0,
            OS=0x40004,
            fileType=0x1,
            subtype=0x0,
            date=(0, 0)
        ),
        kids=[
            StringFileInfo(
                [
                    StringTable(
                        '040904B0',
                        [
                            StringStruct('CompanyName', 'v-i.dev'),
                            StringStruct('FileDescription', 'Thunderbird Usenet Newsgroup Import Converter'),
                            StringStruct('OriginalFilename', 'tunic.exe'),
                            StringStruct('FileVersion', build.VERSION_STR),
                            StringStruct('InternalName', 'tunic'),
                            StringStruct('ProductName', 'TUNIC v' + build.VERSION_STR),
                            StringStruct('ProductVersion', build.VERSION_STR)
                        ]
                    )
                ]
            ),
            VarFileInfo(
                [
                    VarStruct('Translation', [1033, 1200])
                ]
            )
        ]
    )

analysis = Analysis(
    build.PY_FILES,
    pathex=[],
    binaries=[],
    datas=extra_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0
)

pyz = PYZ(analysis.pure, analysis.zipped_data)

exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name='TUNIC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',
    codesign_identity=None,
    entitlements_file=None,
    icon=[str(icon)],
    contents_directory='.',
    version=version
)

coll = COLLECT(
    exe,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TUNIC'
)

if platform == OS.MAC:
    info_plist = {
        'NSUIElement': 1,
        'NSPrincipalClass': 'NSApplication',
        'HSHighResolutionCapable': True,
        'CFBundleDisplayName': 'TUNIC',
        'CFBundleExecutable': 'TUNIC',
        'CFBundleIconFile': build.ICON_MAC.name,
        'CFBundleIdentifier': 'dev.v-i.tunic',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': build.VERSION_STR,
    }

    app = BUNDLE(
        coll,
        name='TUNIC.app',
        icon=str(icon),
        bundle_identifier='dev.v-i.tunic',
        info_plist=info_plist
    )
