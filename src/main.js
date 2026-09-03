const { app, BrowserWindow, ipcMain, Tray, Menu, nativeImage } = require('electron');
const path = require('path');
const fs = require('fs');

let win;
let tray;
let isQuitting = false;

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
      nodeIntegration: false
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
ipcMain.handle('load-solutions', () => {
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

ipcMain.on('window-minimize', () => win && win.minimize());
ipcMain.on('window-close', () => win && win.hide());

app.whenReady().then(() => {
  // Menu-bar-style app: live in the tray rather than cluttering the dock.
  if (process.platform === 'darwin' && app.dock) app.dock.hide();

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
