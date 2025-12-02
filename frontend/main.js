const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let backendProcess = null;

function startBackend() {
  const backendPath = path.join(process.resourcesPath, "backend", "py_server_start.exe");

  console.log("Launching backend at:", backendPath);

  backendProcess = spawn(backendPath, [], {
    cwd: path.dirname(backendPath),     // IMPORTANT: ensure correct working directory
    detached: false,
    shell: false
  });

  backendProcess.stdout?.on("data", (data) => {
    console.log("[DJANGO STDOUT]", data.toString());
  });

  backendProcess.stderr?.on("data", (data) => {
    console.error("[DJANGO STDERR]", data.toString());
  });

  backendProcess.on("error", (err) => {
    console.error("[BACKEND ERROR]", err);
  });

  backendProcess.on("exit", (code, signal) => {
    console.error(`[BACKEND EXIT] code=${code}, signal=${signal}`);
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  // Load Django backend UI
  win.loadURL("http://127.0.0.1:8000");
}

app.whenReady().then(() => {
  startBackend();
  createWindow();
});

app.on("before-quit", () => {
  if (backendProcess) {
    console.log("Killing backend process...");
    backendProcess.kill();
  }
});
