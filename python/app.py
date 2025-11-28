import os
import sys
import subprocess
import webbrowser
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Ensure database migrations are applied
subprocess.run([sys.executable, "manage.py", "migrate"])

# Start Django server in background
server = subprocess.Popen(
    [sys.executable, "manage.py", "runserver", "127.0.0.1:8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Wait a bit for server to start
time.sleep(2)

# Open the default browser (or Electron window later) to the homepage
webbrowser.open("http://127.0.0.1:8000")

# Keep the script running until user closes the app
try:
    server.wait()
except KeyboardInterrupt:
    server.terminate()
