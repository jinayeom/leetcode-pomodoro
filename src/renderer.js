// ------------------------------------------------------------------
//  Pomodoro Focus — renderer
// ------------------------------------------------------------------

const els = {
  body: document.body,
  countdown: document.getElementById('countdown'),
  modePill: document.getElementById('modePill'),
  cycleInfo: document.getElementById('cycleInfo'),
  startBtn: document.getElementById('startBtn'),
  resetBtn: document.getElementById('resetBtn'),
  skipBtn: document.getElementById('skipBtn'),
  settingsBtn: document.getElementById('settingsBtn'),
  minBtn: document.getElementById('minBtn'),
  closeBtn: document.getElementById('closeBtn'),
  settingsOverlay: document.getElementById('settingsOverlay'),
  focusInput: document.getElementById('focusInput'),
  breakInput: document.getElementById('breakInput'),
  saveSettings: document.getElementById('saveSettings'),
  cancelSettings: document.getElementById('cancelSettings'),
  codeHeader: document.getElementById('codeHeader'),
  codeScroll: document.getElementById('codeScroll')
};

// ---------- Persisted settings ----------
const settings = {
  focus: Number(localStorage.getItem('focusMin')) || 25,
  break: Number(localStorage.getItem('breakMin')) || 5
};

// ---------- Timer state ----------
let mode = 'focus';        // 'focus' | 'break'
let remaining = settings.focus * 60;
let running = false;
let round = 1;
let tickHandle = null;

function fmt(sec) {
  const m = String(Math.floor(sec / 60)).padStart(2, '0');
  const s = String(sec % 60).padStart(2, '0');
  return `${m}:${s}`;
}

function render() {
  els.countdown.textContent = fmt(remaining);
  els.modePill.textContent = mode === 'focus' ? 'Focus' : 'Break';
  els.cycleInfo.textContent = mode === 'focus' ? `Round ${round}` : 'Break time';
  els.startBtn.textContent = running ? 'Pause' : 'Start';
}

function tick() {
  if (remaining > 0) {
    remaining--;
    render();
  } else {
    switchMode();
  }
}

function start() {
  if (running) { pause(); return; }
  running = true;
  tickHandle = setInterval(tick, 1000);
  render();
}

function pause() {
  running = false;
  clearInterval(tickHandle);
  render();
}

function reset() {
  pause();
  remaining = (mode === 'focus' ? settings.focus : settings.break) * 60;
  render();
}

function switchMode() {
  pause();
  if (mode === 'focus') {
    mode = 'break';
    remaining = settings.break * 60;
  } else {
    mode = 'focus';
    round++;
    remaining = settings.focus * 60;
  }
  render();
  notify();
  start(); // auto-continue into the next interval
}

function notify() {
  try {
    new Notification('Pomodoro Focus', {
      body: mode === 'focus' ? `Round ${round} — time to focus!` : 'Break time — step away.'
    });
  } catch (_) { /* notifications optional */ }
}

// ---------- Wire up controls ----------
els.startBtn.onclick = start;
els.resetBtn.onclick = reset;
els.skipBtn.onclick = switchMode;
els.minBtn.onclick = () => window.api.minimize();
els.closeBtn.onclick = () => window.api.close();

els.settingsBtn.onclick = () => {
  els.focusInput.value = settings.focus;
  els.breakInput.value = settings.break;
  els.settingsOverlay.classList.add('open');
};
els.cancelSettings.onclick = () => els.settingsOverlay.classList.remove('open');
els.saveSettings.onclick = () => {
  settings.focus = Math.max(1, Number(els.focusInput.value) || 25);
  settings.break = Math.max(1, Number(els.breakInput.value) || 5);
  localStorage.setItem('focusMin', settings.focus);
  localStorage.setItem('breakMin', settings.break);
  els.settingsOverlay.classList.remove('open');
  reset();
};

// ---------- Focus / idle (translucent) toggle ----------
window.api.onWindowFocus((focused) => {
  els.body.classList.toggle('active', focused);
  els.body.classList.toggle('idle', !focused);
});

// "Start Focus Timer" from the tray menu — begin a run if not already going.
window.api.onTrayStart(() => {
  if (!running) start();
});

// ------------------------------------------------------------------
//  Background code scroller
// ------------------------------------------------------------------
let problems = [];
let probIndex = 0;
let scrollY = 0;
let rafId = null;
const SPEED = 0.35; // pixels per frame

function loadProblem(i) {
  if (!problems.length) return;
  const p = problems[i % problems.length];
  els.codeHeader.textContent = `# ${p.id ? p.id + '. ' : ''}${p.title}`;
  // Repeat the snippet so the loop always has content filling the viewport.
  els.codeScroll.textContent = p.solution + '\n\n\n';
  scrollY = -60; // start slightly above so it eases in
}

function animateScroll() {
  scrollY += SPEED;
  els.codeScroll.style.transform = `translateY(${-scrollY}px)`;

  // When the current snippet has fully scrolled past, advance to the next.
  const contentHeight = els.codeScroll.scrollHeight;
  if (scrollY > contentHeight) {
    probIndex = (probIndex + 1) % problems.length;
    loadProblem(probIndex);
  }
  rafId = requestAnimationFrame(animateScroll);
}

async function initCode() {
  problems = await window.api.loadSolutions();
  if (!problems.length) {
    els.codeHeader.textContent = '# Add solutions to solutions.json';
    els.codeScroll.textContent =
      '# No problems loaded yet.\n# See README.md for the database format.';
    return;
  }
  loadProblem(0);
  animateScroll();
}

// ---------- Boot ----------
render();
initCode();
