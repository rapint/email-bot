// backendLauncher.js
const path = require("path");
const { spawn } = require("child_process");

let backendProcess = null;

function startBackend() {
  // Path to bundled backend exe
  const backendPath = path.join(process.resourcesPath, "backend", "py_server_start.exe");

  console.log("Launching backend at:", backendPath);

  backendProcess = spawn(backendPath, [], {
    cwd: path.dirname(backendPath),   // VERY IMPORTANT
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
    console.error(`[BACKEND EXIT] code=${code} signal=${signal}`);
  });

  return backendProcess;
}

module.exports = { startBackend };
