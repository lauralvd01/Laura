# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['App.py', 'Config.py', 'DeleteRender.py', 'NewRender.py', 'PopUP.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\LEVRAUDLaura\\Seb\\_internal\\Files\\arret_par_cle.bat', '.\\Files\\'), ('D:\\LEVRAUDLaura\\Seb\\_internal\\Files\\connexion_par_cle.bat', '.\\Files\\'), ('D:\\LEVRAUDLaura\\Seb\\_internal\\Files\\GENERATION_CLES.bat', '.\\Files\\'), ('D:\\LEVRAUDLaura\\Seb\\_internal\\Files\\restart_par_cle.bat', '.\\Files\\'), ('D:\\LEVRAUDLaura\\Seb\\_internal\\Files\\GENERATION_CLES.bat', '.\\Files\\'), ('D:\\LEVRAUDLaura\\Seb\\_internal\\Files\\green.png', '.\\Files\\'), ('D:\\LEVRAUDLaura\\Seb\\_internal\\Files\\GENERATION_CLES.bat', '.\\Files\\'), ('D:\\LEVRAUDLaura\\Seb\\_internal\\Files\\red.png', '.\\Files\\')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='App',
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
    name='App',
)
