const { app, BrowserWindow, ipcMain, Tray, Menu, nativeImage, session } = require('electron');
const path = require('path');
const fs = require('fs');

let win;
let tray;
let isQuitting = false;

const NORMAL_WIDTH = 460;
const WIDE_WIDTH = 820;

function createWindow() {
  win = new BrowserWindow({
    width: 460,
    height: 620,
    minWidth: 360,
    minHeight: 480,
    frame: false,
    transparent: true,
    resizable: true,
    hasShadow: true,
    show: false,
    icon: path.join(__dirname, '..', 'assets', 'icon.png'),
    // macOS native blur behind the window — gives the frosted "widget" look.
    vibrancy: 'under-window',
    visualEffectState: 'followWindow',
    backgroundColor: '#00000000',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false, // keeps web page's JS world separate from Node.js 
                              // / your computer's APIs (can only talk to OS via 
                              // bridge preload.js)
      sandbox: true // runs app's web page in restricted sandbox (prevents 
                    // malicious code from accessing file system)
    }
  });

  win.loadFile(path.join(__dirname, 'index.html'));
  win.once('ready-to-show', () => win.show());

  // Behave like a menu-bar accessory: the × tucks the widget away into the
  // tray instead of quitting the app. Only the tray's "Quit" truly exits.
  win.on('close', (e) => {
    if (!isQuitting) {
      e.preventDefault();
      win.hide();
    }
  });

  // Defense in depth: this app only ever loads its own local files, but if
  // anything ever tried to navigate away or pop a new window, refuse it.
  win.webContents.on('will-navigate', (e, url) => {
    if (url !== win.webContents.getURL()) e.preventDefault();
  });
  win.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
}

// Only the sender we created should ever be able to call our privileged
// IPC handlers — guards against any future window/webContents this app
// doesn't expect making the same calls.
function isTrustedSender(event) {
  return !!win && event.sender === win.webContents;
}

function setWindowWide(wide) {
  if (!win) return;
  const bounds = win.getBounds();
  const targetWidth = wide ? WIDE_WIDTH : NORMAL_WIDTH;
  // Grow/shrink from the center rather than the top-left corner.
  const x = Math.round(bounds.x + (bounds.width - targetWidth) / 2);
  win.setBounds({ x, y: bounds.y, width: targetWidth, height: bounds.height }, true);
}

function toggleWindow() {
  if (!win) return;
  if (win.isVisible() && win.isFocused()) {
    win.hide();
  } else {
    win.show();
    win.focus();
  }
}

function createTray() {
  const icon = nativeImage.createFromPath(
    path.join(__dirname, '..', 'assets', 'trayIconTemplate.png')
  );
  icon.setTemplateImage(true); // lets macOS auto-adjust for light/dark menu bars
  tray = new Tray(icon);
  tray.setToolTip('Pomodoro Focus');

  const menu = Menu.buildFromTemplate([
    { label: 'Show / Hide', click: toggleWindow },
    { type: 'separator' },
    {
      label: 'Start Focus Timer',
      click: () => {
        win.show();
        win.focus();
        win.webContents.send('tray-start');
      }
    },
    { type: 'separator' },
    {
      label: 'Quit Pomodoro Focus',
      click: () => {
        isQuitting = true;
        app.quit();
      }
    }
  ]);
  tray.setContextMenu(menu);
  tray.on('click', toggleWindow);
}

// Load the solutions database from disk. Falls back to an empty list if
// the file is missing or malformed so the app never crashes on launch.
ipcMain.handle('load-solutions', (event) => {
  if (!isTrustedSender(event)) return [];
  const file = path.join(__dirname, '..', 'solutions.json');
  try {
    const raw = fs.readFileSync(file, 'utf-8');
    const data = JSON.parse(raw);
    return Array.isArray(data) ? data : (data.problems || []);
  } catch (err) {
    console.error('Could not read solutions.json:', err.message);
    return [];
  }
});

ipcMain.on('window-minimize', (event) => { if (isTrustedSender(event)) win.minimize(); });
ipcMain.on('window-close', (event) => { if (isTrustedSender(event)) win.hide(); });
ipcMain.on('window-set-wide', (event, wide) => { if (isTrustedSender(event)) setWindowWide(wide); });

app.whenReady().then(() => {
  // Menu-bar-style app: live in the tray rather than cluttering the dock.
  if (process.platform === 'darwin' && app.dock) app.dock.hide();

  // Principle of least privilege: this app never needs camera, mic,
  // geolocation, MIDI, USB, etc. — deny every permission request except the
  // one feature we actually use (desktop notifications between pomodoro
  // rounds).
  session.defaultSession.setPermissionRequestHandler((_wc, permission, callback) => {
    callback(permission === 'notifications');
  });
  session.defaultSession.setPermissionCheckHandler((_wc, permission) => permission === 'notifications');

  createWindow();
  createTray();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
    else toggleWindow();
  });
});

app.on('before-quit', () => { isQuitting = true; });

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
