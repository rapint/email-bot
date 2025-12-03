# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['py_server_start.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # Django project folder
        ('emailbot', 'emailbot'),

        # Django app templates
        ('mailer/templates', 'mailer/templates'),

        # Database file
        ('db.sqlite3', '.'),

        # manage.py
        ('manage.py', '.'),
    ],
    hiddenimports=[
        'django',
        'django.contrib.staticfiles',
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.admin',
        'waitress',
        'groq', 
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='backend_server',
    debug=False,
    strip=False,
    upx=False,
    console=False,      # Hide console window
    icon=None,
)
