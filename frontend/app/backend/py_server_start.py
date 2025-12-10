import os
import sys
import traceback

# Always write logs next to the EXE
try:
    exe_dir = os.path.dirname(sys.executable)
except:
    exe_dir = os.path.dirname(os.path.abspath(__file__))

log_path = os.path.join(exe_dir, "backend.log")

# Open log file (overwrite previous)
log_file = open(log_path, "w", buffering=1)
sys.stdout = log_file
sys.stderr = log_file

log_file.write("=== Backend Starting ===\n")

# Detect PyInstaller directory
if hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

log_file.write(f"BASE_DIR: {BASE_DIR}\n")

os.chdir(BASE_DIR)

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emailbot.settings")
    log_file.write("Django settings loaded\n")

    import django
    django.setup()
    log_file.write("Django setup OK\n")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    log_file.write("WSGI application loaded\n")

    from waitress import serve
    log_file.write("Starting Waitress on 127.0.0.1:8000\n")

    serve(application, host="127.0.0.1", port=8000)

except Exception as e:
    log_file.write("\n=== ERROR OCCURRED ===\n")
    log_file.write(str(e) + "\n")
    log_file.write(traceback.format_exc())
    log_file.flush()
    raise
