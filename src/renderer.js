// ------------------------------------------------------------------
//  Pomodoro Focus — renderer
// ------------------------------------------------------------------

const els = {
  countdown: document.getElementById('countdown'),
  modePill: document.getElementById('modePill'),
  cycleInfo: document.getElementById('cycleInfo'),
  startBtn: document.getElementById('startBtn'),
  resetBtn: document.getElementById('resetBtn'),
  skipBtn: document.getElementById('skipBtn'),
  settingsBtn: document.getElementById('settingsBtn'),
  widenBtn: document.getElementById('widenBtn'),
  minBtn: document.getElementById('minBtn'),
  closeBtn: document.getElementById('closeBtn'),
  settingsOverlay: document.getElementById('settingsOverlay'),
  focusInput: document.getElementById('focusInput'),
  breakInput: document.getElementById('breakInput'),
  saveSettings: document.getElementById('saveSettings'),
  cancelSettings: document.getElementById('cancelSettings'),
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

let isWide = false;
els.widenBtn.onclick = () => {
  isWide = !isWide;
  window.api.setWide(isWide);
  els.widenBtn.textContent = isWide ? '⤡' : '⤢';
  els.widenBtn.title = isWide ? 'Narrow' : 'Widen';
};

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

// "Start Focus Timer" from the tray menu — begin a run if not already going.
window.api.onTrayStart(() => {
  if (!running) start();
});

// ------------------------------------------------------------------
//  Background code scroller — a single continuous loop of
//  "# id. Title" headers each followed by their solution, with no
//  gaps between problems.
// ------------------------------------------------------------------
let scrollY = 0;
let loopHeight = 0;
let rafId = null;
const SPEED = 0.35; // pixels per frame

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function blockHTML(p) {
  const header = `# ${p.id ? p.id + '. ' : ''}${p.title}`;
  return `<div class="code-block">` +
    `<div class="block-header">${escapeHtml(header)}</div>` +
    `<pre class="block-code">${escapeHtml(p.solution)}</pre>` +
    `</div>`;
}

function animateScroll() {
  scrollY += SPEED;
  // Content is duplicated back-to-back, so subtracting exactly one
  // copy's height keeps the motion continuous with no visible seam.
  if (loopHeight > 0 && scrollY >= loopHeight) {
    scrollY -= loopHeight;
  }
  els.codeScroll.style.transform = `translateY(${-scrollY}px)`;
  rafId = requestAnimationFrame(animateScroll);
}

async function initCode() {
  const problems = await window.api.loadSolutions();
  if (!problems.length) {
    els.codeScroll.innerHTML =
      '<div class="code-block"><div class="block-header"># Add solutions to solutions.json</div></div>';
    return;
  }
  const html = problems.map(blockHTML).join('');
  // Two copies back-to-back give the loop somewhere identical to land
  // on when it wraps, so the transition is invisible.
  els.codeScroll.innerHTML = html + html;

  requestAnimationFrame(() => {
    loopHeight = els.codeScroll.scrollHeight / 2;
    animateScroll();
  });
}

// ---------- Boot ----------
render();
initCode();
