// main.js
const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let pyProc = null;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: { contextIsolation: true }
  });
  win.loadURL('http://127.0.0.1:8000');
}

function startPythonServer() {
  const script = path.join(__dirname, 'py_server_start.py');
  pyProc = spawn('python', [script]);

  pyProc.stdout.on('data', (data) => console.log(`Django: ${data}`));
  pyProc.stderr.on('data', (data) => console.error(`Django Error: ${data}`));
}

app.whenReady().then(() => {
  startPythonServer();
  // give Django a second to start, then open window
  setTimeout(createWindow, 2500);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('quit', () => {
  if (pyProc) pyProc.kill();
});
