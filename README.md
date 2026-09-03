<img width="852" height="627" alt="leetcode pomodoro" src="https://github.com/user-attachments/assets/debeabbf-a907-468c-9bc7-0fbe44d93cce" />

# Pomodoro Focus

A glassmorphic desktop Pomodoro timer inspired by the macOS/iOS widget aesthetic.

- **Translucent, frosted-glass bubble** in a deep blue–indigo gradient.
- **Configurable** focus & break durations (gear icon → Settings).
- **Large center countdown** (~20% of the window height).
- **Scrolling Python code** backdrop — a single continuous loop through all
  **75** LeetCode **Grind 75** solutions, each problem's header immediately
  followed by its solution with no gaps in between.
- **Lives in the menu bar** — a tray icon lets you show/hide the widget or
  quit; the × on the window just tucks it away instead of closing the app.

## Install

### Option A: Download the app (recommended)

Grab the latest `.dmg` from the [Releases page](https://github.com/jinayeom/leetcode-pomodoro/releases) —
pick the `arm64` build for Apple Silicon Macs or the plain build for Intel
Macs. Open the `.dmg` and drag **LeetCode Pomodoro** into Applications.

This build isn't code-signed or notarized (that requires a paid Apple
Developer account), so macOS Gatekeeper will refuse to open it with a
message like *"LeetCode Pomodoro" can't be opened because Apple cannot check
it for malicious software*. To run it anyway:

1. **Right-click** (or Control-click) **LeetCode Pomodoro.app** in
   Applications and choose **Open**.
2. In the dialog that appears, click **Open** again.

You only need to do this once — after that it opens normally, including via
Spotlight or the Dock.

### Option B: Run from source

Requires [Node.js](https://nodejs.org/) 18+ (includes `npm`).

```bash
git clone https://github.com/jinayeom/leetcode-pomodoro.git
cd leetcode-pomodoro
npm install
npm start
```

Either way, the app launches as a frameless, translucent indigo window and
adds an icon to your menu bar (it won't show in the dock). Drag the widget by
its top bar.

### Menu bar controls

Click the tray icon to show/hide the widget, or right-click (or left-click,
depending on your macOS settings) for a menu with **Show/Hide**,
**Start Focus Timer**, and **Quit Pomodoro Focus**. Quitting from the tray is
the only way to fully exit — closing the window just hides it.

## The solutions database

Solutions live in **`solutions.json`** at the project root — a plain JSON
array, one object per problem. It already ships with all **75** Grind 75
problems, generated from the `raw_solutions/` folder (one real `.py` file per problem,
e.g. `raw_solutions/1_two-sum.py`).

```json
[
  {
    "id": 1,
    "title": "Two Sum",
    "difficulty": "Easy",
    "solution": "class Solution:\n    def twoSum(self, nums, target):\n        ..."
  }
]
```

| Field        | Required | Notes                                                        |
|--------------|----------|--------------------------------------------------------------|
| `id`         | optional | LeetCode problem number, shown in the header.                |
| `title`      | **yes**  | Problem name, shown in the header.                           |
| `difficulty` | optional | Not displayed in the UI yet; handy metadata for later.       |
| `solution`   | **yes**  | The Python code that scrolls. Use `\n` for line breaks.      |

### Editing or adding solutions

`solutions.json` is generated — don't hand-edit it. Instead:

1. Edit or add an entry in the `PROBLEMS` list at the top of
   **`generate_solutions.py`** (or drop a new file straight into `raw_solutions/` named
   `<id>-or-anything_<slug>.py`).
2. Re-run the generator:

   ```bash
   python3 generate_solutions.py
   ```

   This rewrites every file in `raw_solutions/` from `PROBLEMS` and rebuilds
   `solutions.json` from whatever's in `raw_solutions/` — so hand-added files there also
   get picked up on the next run.

The full Grind 75 list (for reference) is at
<https://www.techinterviewhandbook.org/grind75>.

## Building a release

Packaging is handled by [electron-builder](https://www.electron.build/), configured
in the `build` field of `package.json`.

```bash
npm install
CSC_IDENTITY_AUTO_DISCOVERY=false npm run dist
```

That produces two unsigned `.dmg` files in `release/` — one for Apple Silicon
(`arm64`) and one for Intel (`x64`). The `CSC_IDENTITY_AUTO_DISCOVERY=false`
env var tells electron-builder not to look for a code-signing certificate,
since this project isn't signed/notarized. To publish a new version:

1. Bump `version` in `package.json`.
2. Run the build command above.
3. Create a new [GitHub Release](https://github.com/jinayeom/leetcode-pomodoro/releases/new),
   tag it (e.g. `v1.0.1`), and attach both `.dmg` files from `release/`.

## Customizing

- **Scroll speed** — `SPEED` constant near the bottom of `src/renderer.js`.
- **Colors** — the `:root` variables at the top of `src/styles.css`
  (`--bg-1` / `--bg-2` / `--bg-3` for the indigo gradient).
- **Countdown size** — the `.countdown { font-size: 20vh }` rule in
  `src/styles.css`.
- **Window size** — `width` / `height` in `src/main.js`.
- **Tray icon** — regenerate `assets/trayIconTemplate.png` /
  `@2x.png` with any monochrome silhouette; macOS auto-adjusts template
  images for light/dark menu bars.
