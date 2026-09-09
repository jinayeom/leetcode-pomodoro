const { contextBridge, ipcRenderer } = require('electron');

// Minimal, safe bridge between the renderer UI and the main process.
contextBridge.exposeInMainWorld('api', {
  loadSolutions: () => ipcRenderer.invoke('load-solutions'),
  onTrayStart: (cb) => ipcRenderer.on('tray-start', () => cb()),
  minimize: () => ipcRenderer.send('window-minimize'),
  close: () => ipcRenderer.send('window-close'),
  setWide: (wide) => ipcRenderer.send('window-set-wide', wide)
});
