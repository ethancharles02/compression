import PyInstaller.__main__

PyInstaller.__main__.run([
    'src/__main__.py',
    '-n', 'Compressor',
    '--onefile',
    '--distpath', '.',
    '--noconsole',
    '--clean'
])