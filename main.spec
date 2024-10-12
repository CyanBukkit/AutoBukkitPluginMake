# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.win32 import versioninfo

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('view', '.'), ('core', '.'), ('role', '.'), ('./view/main.ui', 'view'), ('./view/logo.ico', 'view')],
    hiddenimports=['core', 'role', 'view'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

# 创建版本信息对象
vi = versioninfo.VSVersionInfo(
    ffi=versioninfo.FixedFileInfo(
        filevers=(1, 0, 1, 0),
        prodvers=(1, 0, 1, 0),
        mask=0x3F,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        versioninfo.StringFileInfo(
            [
                versioninfo.StringTable(
                    '040904B0',
                    [
                        versioninfo.StringStruct('CompanyName', 'CyanBukkit'),
                        versioninfo.StringStruct('FileDescription', 'Ai Bukkit'),
                        versioninfo.StringStruct('FileVersion', '1.0.1.0'),
                        versioninfo.StringStruct('InternalName', 'Ai Bukkit'),
                        versioninfo.StringStruct('OriginalFilename', 'Ai Bukkit'),
                        versioninfo.StringStruct('ProductName', 'Ai Bukkit'),
                        versioninfo.StringStruct('ProductVersion', '1.0.1.0')
                    ]
                )
            ]
        ),
        versioninfo.VarFileInfo([versioninfo.VarStruct('Translation', [0x0409, 0x04B0])])
    ]
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Ai Bukkit-1.0.1.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['E:\\Python\\AutoWriteProject\\view\\logo.ico'],
    version=vi,  # 添加版本信息
)