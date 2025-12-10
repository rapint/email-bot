const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const net = require("net");

let backendProcess = null;
const BACKEND_PORT = 8000;

function isBackendRunning() {
  return new Promise((resolve) => {
    const socket = net.createConnection(BACKEND_PORT, "127.0.0.1");
    socket.on("connect", () => {
      socket.end();
      resolve(true);
    });
    socket.on("error", () => resolve(false));
  });
}

async function waitForBackend() {
  let tries = 0;

  while (!(await isBackendRunning())) {
    tries++;
    if (tries > 40) throw new Error("Backend failed to start");
    await new Promise((r) => setTimeout(r, 250));
  }
}

function startBackend() {
  let backendPath;

  if (!app.isPackaged) {
    // DEV MODE
    backendPath = path.join(__dirname, "app", "backend", "dist", "backend_server.exe");
  } else {
    // PRODUCTION MODE
    backendPath = path.join(process.resourcesPath, "backend", "backend_server.exe");
  }

  backendProcess = spawn(backendPath, [], {
    detached: false
  });

  backendProcess.stdout?.on("data", (d) => console.log("[BACKEND]", d.toString()));
  backendProcess.stderr?.on("data", (d) => console.error("[BACKEND ERROR]", d.toString()));
}

async function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  // Wait until backend is actually running
  await waitForBackend();

  win.loadURL("http://127.0.0.1:8000");
}

app.whenReady().then(() => {
  startBackend();
  createWindow();
});

app.on("before-quit", () => {
  if (backendProcess) {
    backendProcess.kill();
  }
});
