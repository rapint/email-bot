import os
import shutil

# This script lives in D:\workspace\Email-bot\prepare_python_portable.py
# So BASE_DIR = D:\workspace\Email-bot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct relative path to your backend
BACKEND_DIR = os.path.join(BASE_DIR, "frontend", "app", "backend")

PYTHON_SOURCE = os.path.join(BACKEND_DIR, "python")
PYTHON_DEST = os.path.join(BACKEND_DIR, "python_portable")

print("BASE_DIR =", BASE_DIR)
print("BACKEND_DIR =", BACKEND_DIR)
print("PYTHON_SOURCE =", PYTHON_SOURCE)

if not os.path.exists(PYTHON_SOURCE):
    raise FileNotFoundError(f"ERROR: Python folder not found at: {PYTHON_SOURCE}")

if os.path.exists(PYTHON_DEST):
    shutil.rmtree(PYTHON_DEST)

print("Copying Python runtime → python_portable...")
shutil.copytree(PYTHON_SOURCE, PYTHON_DEST)

print("✔ DONE. python_portable created successfully!")
