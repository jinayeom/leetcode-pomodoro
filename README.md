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

## Requirements

- [Node.js](https://nodejs.org/) 18+ (includes `npm`)

## Setup

```bash
cd pomodoro-focus
npm install
npm start
```

The app launches as a frameless, translucent indigo window and adds an icon to
your menu bar (it won't show in the dock). Drag the widget by its top bar.

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
