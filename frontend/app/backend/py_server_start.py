import os
import sys
import subprocess

# Determine base directory (PyInstaller bundle or dev)
if hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)

# Path to embedded python interpreter (NOT sys.executable)
python_path = os.path.join(BASE_DIR, "python_portable", "python.exe")
manage_path = os.path.join(BASE_DIR, "manage.py")

print("BASE_DIR:", BASE_DIR)
print("Using python:", python_path)
print("Using manage.py:", manage_path)
print("CWD:", os.getcwd())

# Run migrations safely
try:
    subprocess.run([python_path, manage_path, "migrate"], check=False)
except Exception as e:
    print("Migration error:", e)

# Start Django server
subprocess.run([python_path, manage_path, "runserver", "127.0.0.1:8000"])
