# py_server_start.py
import os, sys, subprocess, time

BASE_DIR = os.path.join(os.path.dirname(__file__), 'python')
os.chdir(BASE_DIR)

# Apply migrations once to ensure DB setup (optional)
subprocess.run([sys.executable, 'manage.py', 'migrate'])

# Start server
subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])
