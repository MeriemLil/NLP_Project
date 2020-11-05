# -*- mode: python -*-

block_cipher = None


a = Analysis(['/home/lauri/project/NLP_Project/src/main/python/main.py'],
             pathex=['/home/lauri/project/NLP_Project/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/home/lauri/nlpEnv/lib/python3.7/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/home/lauri/project/NLP_Project/target/PyInstaller/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='nlp_project',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='nlp_project')
