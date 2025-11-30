// main.js
const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

let pyProc = null;

// FULL PATH to venv Python
const PYTHON = "D:/workspace/Email-bot/backend(Django)/venv/Scripts/python.exe";

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: { contextIsolation: true }
    });

    win.loadURL("http://127.0.0.1:8000");
}

function startPythonServer() {
    const script = path.join(__dirname, "py_server_start.py");

    // RUN DJANGO USING VENV PYTHON
    pyProc = spawn(PYTHON, [script], {
        cwd: "D:/workspace/Email-bot/backend(Django)",
        shell: false
    });

    pyProc.stdout.on("data", data => console.log(`Django: ${data}`));
    pyProc.stderr.on("data", data => console.error(`Django Error: ${data}`));
}

app.whenReady().then(() => {
    startPythonServer();
    setTimeout(createWindow, 2500);
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});

app.on("quit", () => {
    if (pyProc) pyProc.kill();
});
