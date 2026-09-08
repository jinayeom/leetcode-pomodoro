const js = require('@eslint/js');
const globals = require('globals');

module.exports = [
  js.configs.recommended,
  {
    // Electron main process + preload script: Node/CommonJS environment.
    files: ['src/main.js', 'src/preload.js'],
    languageOptions: {
      sourceType: 'commonjs',
      globals: globals.node
    }
  },
  {
    // Renderer script: runs in the browser window, not Node (sandboxed,
    // contextIsolation on). `api` comes from preload's contextBridge.
    files: ['src/renderer.js'],
    languageOptions: {
      sourceType: 'script',
      globals: { ...globals.browser, api: 'readonly' }
    }
  }
];
