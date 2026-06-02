# <img src="assets/icon.png" width="48" height="48" valign="middle"> Scribly

[![Python Version](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/UI-CustomTkinter-darkblue?style=flat-square&logo=visualstudiocode&logoColor=cyan)](https://github.com/tomschimanek/customtkinter)
[![Pygments Highlighting](https://img.shields.io/badge/Syntax-Pygments-green?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEyIDJMMS41IDcuNWwzLjU4IDEuNzlMMi42MyAxMGwxMC4zNyA1LjE4TDIzLjM3IDEwTDIwLjMxIDkuMjlMMjIuNSA3LjVMMTIgMnptMCA1LjhjLTEuMDEgMC0xLjgzLS44Mi0xLjgzLTEuODNTMTAuOTkgNC4xNyAxMiA0LjE3czEuODMuODIgMS44MyAxLjgzcy0uODIgMS44My0xLjgzIDEuODN6bTAgNC42Yy0xLjI0IDAtMi4yNS0xLjAxLTIuMjUtMi4yNVMxMC43NiAxMC4xMiAxMiAxMC4xMnMyLjI1IDEuMDEgMi4yNSAyLjI1cy0xLjAxIDIuMjUtMi4yNSAyLjI1eiIvPjwvc3ZnPg==&logoColor=white)](https://pygments.org/)
[![OS Support](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)](https://github.com/SuryaK999/Scribly-Text-Editor-App)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Scribly is a distraction-free, minimalist, yet feature-rich desktop text editor built with Python and CustomTkinter. It resembles native modern OS editors (like Linux Gedit or Windows Notepad) while integrating professional developer utilities such as real-time syntax highlighting, custom theme designs, and bracket matching.

---

## 🚀 Key Features

* 🎨 **Unified Flat Theme Engine**: Blends the toolbar into the document canvas with seamless 1-pixel separators. Includes 6 built-in presets (One Dark, Monokai, Cyberpunk, Solarized Light/Dark, Github Light) and a custom theme builder.
* ✍️ **Syntax Highlighting**: Real-time syntax styling using **Pygments** (supports Python, Markdown, HTML, CSS, JavaScript, JSON, etc.) debounced at 100ms to eliminate typing latency.
* 🔢 **Smart Line Numbers**: Column-synced sidebar that dynamically scales width to line digits and handles wrapped line alignments flawlessly. Highlights the active line number.
* ⚙️ **Custom Theme Creator Dialog**: Visual designer (`+ Custom Theme`) allowing real-time OS color picking for background, text, cursor, selections, and syntax highlight categories, exporting configurations directly as JSON.
* ⚡ **Developer Conveniences**:
  * **Auto-closing pairs** for brackets `() {} []` and quotes `"" ''`.
  * **Smart backspace** deleting adjacent closing brackets.
  * **Bracket matching** depth-scans and highlights matching pairs under the cursor.
  * **Auto-indentation** matching previous indentation levels and indenting automatically after code-block entries (e.g., lines ending in `:`).
* 🔍 **Find & Replace panel**: Slides in from the bottom with match counters (`X of Y`), case-sensitive filtering, whole-word matching, regular expression queries, and bulk reverse-order "Replace All".
* 📂 **Workspace Explorer Sidebar**: Collapsible file tree that allows you to double-click and open files, optimized with directory lazy-loading.

---

## 🖼️ Image Showcase

Add screenshots to the `docs/screenshots/` folder to populate these visuals on GitHub:

| 🖥️ Main Workspace (Zen Mode) | 🎨 Visual Theme Customizer |
| :---: | :---: |
| <img src="assets/icon.png" width="220" alt="Main Editor Preview"><br>_Placeholder: Add `docs/screenshots/editor_preview.png` here_ | <img src="assets/icon.png" width="220" alt="Theme Creator Dialog"><br>_Placeholder: Add `docs/screenshots/theme_creator.png` here_ |

| 🔍 Advanced Find & Replace Panel | 📁 Workspace Explorer Sidebar |
| :---: | :---: |
| <img src="assets/icon.png" width="220" alt="Find Replace Preview"><br>_Placeholder: Add `docs/screenshots/search_preview.png` here_ | <img src="assets/icon.png" width="220" alt="Workspace Tree Sidebar"><br>_Placeholder: Add `docs/screenshots/sidebar_preview.png` here_ |

---

## 🛠️ Installation

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Clone the Repository
```bash
git clone https://github.com/SuryaK999/Scribly-Text-Editor-App.git
cd Scribly-Text-Editor-App
```

### 3. Set Up Virtual Environment
```bash
python -m venv .venv
# On Windows (PowerShell)
.venv\Scripts\Activate.ps1
# On Windows (cmd)
.venv\Scripts\activate.bat
# On macOS / Linux
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Application

Launch the editor with Python:
```bash
python main.py
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + N` | Create a New File |
| `Ctrl + O` | Open a File |
| `Ctrl + S` | Save the Current File |
| `Ctrl + Shift + S` | Save File As |
| `Ctrl + F` | Toggle Find & Replace Panel |
| `Ctrl + B` | Toggle Workspace Sidebar |
| `Ctrl + Z` | Undo |
| `Ctrl + Y` | Redo |
| `Ctrl + Plus / Minus` | Zoom Font In / Out |
| `Ctrl + MouseWheel` | Dynamic Font Zoom |
| `Ctrl + W` / `Ctrl + Q` | Exit Application |

---

## 📁 File Structure

```text
Scribly/
├── assets/
│   ├── icon.png        # Cross-platform high-resolution icon
│   ├── icon.ico        # Multi-resolution Windows application icon
│   └── icon.icns       # Multi-resolution macOS bundle icon
├── components/
│   ├── editor_area.py  # Code editor viewport & bindings
│   ├── file_tree.py    # Lazy-loading directory tree widget
│   ├── find_replace.py # Floating find/replace query panel
│   ├── line_numbers.py # Canvas-drawn dynamic scroll-synced line indices
│   ├── status_bar.py   # Position and document statistic bar
│   └── theme_dialog.py # Custom theme creator modal
├── main.py             # App entrance & layout manager
├── theme_manager.py    # Theme loader database & Pygments style mapping
├── requirements.txt    # Library dependencies
└── .gitignore          # Files excluded from VCS tracking
```

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
