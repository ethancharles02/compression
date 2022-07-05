import PyInstaller.__main__

PyInstaller.__main__.run([
    '__main__.py',
    '-n',
    'Compressor',
    '--onefile',
    '--noconsole'
])