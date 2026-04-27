# -*- mode: python ; coding: utf-8 -*-

SITE_PACKAGES = '\Local\\Packages\\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python39\\site-packages'

a = Analysis(
    ['run.py'],
    pathex=[SITE_PACKAGES],
    binaries=[
        (SITE_PACKAGES + '\\_curses.cp39-win_amd64.pyd', '.'),
        (SITE_PACKAGES + '\\_curses_panel.cp39-win_amd64.pyd', '.'),
    ],
    datas=[],
    hiddenimports=[
        'windows_curses',
        '_curses',
        '_curses_panel',
        'feedparser',
        'feedparser.datetimes',
        'feedparser.encodings',
        'feedparser.html',
        'feedparser.http',
        'feedparser.namespaces',
        'feedparser.parsers',
        'feedparser.sgml',
        'feedparser.urls',
        'sgmllib',
        'requests',
        'certifi',
        'charset_normalizer',
        'idna',
        'urllib3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='newsfeed',
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
)
