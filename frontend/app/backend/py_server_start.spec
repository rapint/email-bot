# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['py_server_start.py'],
    pathex=[],
    binaries=[],
    datas=[('manage.py', '.'), ('db.sqlite3', '.'), ('emailbot', 'emailbot'), ('mailer', 'mailer'), ('python_portable', 'python_portable')],
    hiddenimports=['django'],
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
    [],
    exclude_binaries=True,
    name='py_server_start',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='py_server_start',
)
