<p align="center">
  <img src="assets/icon.png" width="120" height="120" alt="Scribly Logo">
</p>

<h1 align="center">Scribly</h1>

<p align="center">
  <em>A distraction-free, feature-rich desktop text editor built with Python & CustomTkinter</em>
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python_3.8+-3776AB.svg?style=flat-square&logo=python&logoColor=ffdd54" alt="Python 3.8+">
  </a>&nbsp;
  <a href="https://github.com/tomschimanek/customtkinter">
    <img src="https://img.shields.io/badge/CustomTkinter-1a73e8.svg?style=flat-square&logo=tkinter&logoColor=white" alt="CustomTkinter">
  </a>&nbsp;
  <a href="https://pygments.org/">
    <img src="https://img.shields.io/badge/Pygments-8A2BE2.svg?style=flat-square&logo=python&logoColor=white" alt="Pygments">
  </a>&nbsp;
  <a href="https://github.com/SuryaK999/Scribly-Text-Editor-App">
    <img src="https://img.shields.io/badge/Windows%20·%20macOS%20·%20Linux-475569.svg?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHJlY3QgeD0iMiIgeT0iMyIgd2lkdGg9IjIwIiBoZWlnaHQ9IjE0IiByeD0iMiIgcnk9IjIiPjwvcmVjdD48bGluZSB4MT0iOCIgeTE9IjIxIiB4Mj0iMTYiIHkyPSIyMSI+PC9saW5lPjxsaW5lIHgxPSIxMiIgeTE9IjE3IiB4Mj0iMTIiIHkyPSIyMSI+PC9saW5lPjwvc3ZnPg==&logoColor=white" alt="Platform">
  </a>&nbsp;
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/MIT_License-f59e0b.svg?style=flat-square" alt="MIT License">
  </a>
</p>

---

Scribly resembles native modern OS editors (like **Linux Gedit** or **Windows Notepad**) while integrating professional developer utilities — real-time syntax highlighting, a visual custom theme builder, intelligent bracket matching, and a collapsible workspace sidebar.

---

## 🖼️ Screenshots

<table>
  <tr>
    <td align="center" width="50%">
      <img src="docs/screenshots/editor_main.png" alt="Main Editor" width="100%">
      <br><strong>🖥️ Main Workspace</strong>
      <br><sub>Syntax-highlighted editing with smart line numbers</sub>
    </td>
    <td align="center" width="50%">
      <img src="docs/screenshots/theme_creator.png" alt="Theme Creator" width="100%">
      <br><strong>🎨 Custom Theme Creator</strong>
      <br><sub>Visual color picker for every UI element</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="docs/screenshots/find_replace.png" alt="Find and Replace" width="100%">
      <br><strong>🔍 Find & Replace</strong>
      <br><sub>Regex support, match counter, and bulk replace</sub>
    </td>
    <td align="center">
      <img src="docs/screenshots/workspace_sidebar.png" alt="Workspace Sidebar" width="100%">
      <br><strong>📂 Workspace Explorer</strong>
      <br><sub>Lazy-loading file tree with double-click to open</sub>
    </td>
  </tr>
</table>

---

## ✨ Features

<table>
  <tr>
    <td width="50%">

### 🎨 Unified Theme Engine
Blends toolbar, editor, and sidebar into one seamless canvas with 1-pixel separators. Ships with **6 built-in presets**:
- One Dark
- Monokai
- Cyberpunk
- Solarized Light / Dark
- Github Light

Plus a **visual Custom Theme Creator** (`+ Custom Theme` button) with real-time OS color picking — export directly as JSON.

</td>
    <td width="50%">

### ✍️ Syntax Highlighting
Real-time token-level styling powered by **Pygments**, debounced at 100ms for zero typing lag.

**Supported languages include:**
`Python` · `JavaScript` · `HTML` · `CSS` · `Markdown` · `JSON` · and many more auto-detected by file extension.

</td>
  </tr>
  <tr>
    <td>

### ⚡ Developer Conveniences
- **Auto-closing pairs** — `() {} [] "" ''`
- **Smart backspace** — deletes adjacent closing bracket
- **Bracket matching** — depth-scans & highlights matching pair under cursor
- **Auto-indentation** — matches previous indent, auto-indents after `:`

</td>
    <td>

### 🔍 Find & Replace
Slides in from the bottom with:
- Live match counter (`X of Y`)
- Case-sensitive toggle
- Whole-word matching
- **Regular expression** queries
- Bulk reverse-order **Replace All**

</td>
  </tr>
  <tr>
    <td>

### 📂 Workspace Explorer
Collapsible sidebar with a lazy-loading directory tree. Double-click any file to open it directly in the editor. Toggle with **Ctrl+B**.

</td>
    <td>

### 🔢 Smart Line Numbers
Column-synced sidebar that dynamically scales width, handles wrapped-line alignment, and highlights the active line number.

</td>
  </tr>
</table>

---

## 🛠️ Installation

### Prerequisites

- **Python 3.8** or higher — [Download Python](https://www.python.org/downloads/)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/SuryaK999/Scribly-Text-Editor-App.git
cd Scribly-Text-Editor-App

# 2. Create & activate virtual environment
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (cmd)
.venv\Scripts\activate.bat
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Scribly
python main.py
```

---

## 📦 Dependencies

| Package | Version | Purpose |
| :--- | :--- | :--- |
| [customtkinter](https://github.com/tomschimanek/customtkinter) | `≥ 5.2.0` | Modern, themeable GUI framework |
| [Pygments](https://pygments.org/) | `≥ 2.15.0` | Syntax highlighting engine |
| [darkdetect](https://github.com/albertosottile/darkdetect) | `≥ 0.8.0` | OS dark/light mode detection |
| [Pillow](https://python-pillow.org/) | `≥ 9.5.0` | Icon loading & multi-resolution scaling |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + N` | New File |
| `Ctrl + O` | Open File |
| `Ctrl + S` | Save |
| `Ctrl + Shift + S` | Save As |
| `Ctrl + F` | Toggle Find & Replace |
| `Ctrl + B` | Toggle Workspace Sidebar |
| `Ctrl + Z` | Undo |
| `Ctrl + Y` | Redo |
| `Ctrl + X / C / V` | Cut / Copy / Paste |
| `Ctrl + +` / `Ctrl + -` | Zoom In / Out |
| `Ctrl + MouseWheel` | Dynamic Font Zoom |
| `Ctrl + W` / `Ctrl + Q` | Exit Application |

---

## 🗂️ Project Structure

```
Scribly-Text-Editor-App/
│
├── 📁 assets/
│   ├── icon.png             # High-resolution app icon (cross-platform)
│   ├── icon.ico             # Windows taskbar & title bar icon
│   └── icon.icns            # macOS bundle icon
│
├── 📁 components/
│   ├── editor_area.py       # Code editor widget, syntax highlighting, auto-pairs
│   ├── file_tree.py         # Lazy-loading workspace directory tree
│   ├── find_replace.py      # Slide-in find & replace panel
│   ├── line_numbers.py      # Scroll-synced line number sidebar
│   ├── status_bar.py        # Cursor position & document stats bar
│   └── theme_dialog.py      # Visual custom theme creator modal
│
├── 📁 docs/screenshots/
│   ├── editor_main.png      # Main workspace screenshot
│   ├── theme_creator.png    # Theme creator dialog screenshot
│   ├── find_replace.png     # Find & replace panel screenshot
│   └── workspace_sidebar.png # Sidebar file tree screenshot
│
├── main.py                  # Application entry point & layout manager
├── theme_manager.py         # Theme registry, loader & Pygments style mapping
├── requirements.txt         # Python package dependencies
├── .gitignore               # Git exclusion rules
└── README.md                # This file
```

---

## 🖥️ Menu System

Scribly provides a standard OS-native menu bar:

| Menu | Options |
| :--- | :--- |
| **File** | New File · Open File · Open Workspace Folder · Save · Save As · Exit |
| **Edit** | Undo · Redo · Cut · Copy · Paste · Find / Replace |
| **View** | Toggle Workspace Sidebar · Zoom In · Zoom Out |

---

## 🎯 Highlights

<div align="center">

| Feature | Details |
| :---: | :--- |
| 🪟 **Cross-Platform Icons** | Multi-resolution icons (16×16 → 256×256) for crisp rendering on all DPIs |
| 🧩 **Windows Taskbar Grouping** | Custom `AppUserModelID` for proper taskbar icon grouping |
| 💾 **Unsaved Changes Guard** | Prompts to save before closing, opening, or creating new files |
| 🔄 **Live Theme Switching** | Instantly swaps all UI layers — toolbar, editor, sidebar, menus, status bar |
| 📐 **Responsive Layout** | Min size 600×400, default 950×600 with resizable panels |

</div>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <sub>Built with ❤️ using Python & CustomTkinter</sub>
</p>
