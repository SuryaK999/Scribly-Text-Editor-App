import os
import json
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Number, Operator, Token

# Default built-in themes
BUILTIN_THEMES = {
    "One Dark": {
        "is_dark": True,
        "editor_bg": "#282c34",
        "editor_fg": "#abb2bf",
        "editor_select_bg": "#3e4451",
        "editor_insert_color": "#528bff",
        "current_line_bg": "#2c313c",
        "line_numbers_bg": "#282c34",
        "line_numbers_fg": "#4b5263",
        "line_numbers_current_fg": "#c8ccd4",
        "bracket_match_bg": "#3e4451",
        "bracket_match_fg": "#abb2bf",
        "find_match_bg": "#4b5263",
        "find_current_bg": "#61afef",
        "syntax": {
            "keyword": "#c678dd",      # Purple
            "function": "#61afef",     # Blue
            "string": "#98c379",       # Green
            "comment": "#5c6370",      # Grey (Italic)
            "number": "#d19a66",       # Orange
            "operator": "#56b6c2",     # Cyan
            "name": "#e06c75"          # Red
        }
    },
    "Monokai": {
        "is_dark": True,
        "editor_bg": "#272822",
        "editor_fg": "#f8f8f2",
        "editor_select_bg": "#49483e",
        "editor_insert_color": "#f8f8f0",
        "current_line_bg": "#3e3d32",
        "line_numbers_bg": "#272822",
        "line_numbers_fg": "#90908a",
        "line_numbers_current_fg": "#f8f8f2",
        "bracket_match_bg": "#49483e",
        "bracket_match_fg": "#f92672",
        "find_match_bg": "#75715e",
        "find_current_bg": "#a6e22e",
        "syntax": {
            "keyword": "#f92672",      # Pink
            "function": "#a6e22e",     # Green
            "string": "#e6db74",       # Yellow
            "comment": "#75715e",      # Grey
            "number": "#ae81ff",       # Purple
            "operator": "#f92672",     # Pink
            "name": "#66d9ef"          # Cyan
        }
    },
    "Cyberpunk": {
        "is_dark": True,
        "editor_bg": "#1d102f",
        "editor_fg": "#ffffff",
        "editor_select_bg": "#f000ff",
        "editor_insert_color": "#00ffd8",
        "current_line_bg": "#2d1b4e",
        "line_numbers_bg": "#1d102f",
        "line_numbers_fg": "#604780",
        "line_numbers_current_fg": "#00ffd8",
        "bracket_match_bg": "#00ffd8",
        "bracket_match_fg": "#1d102f",
        "find_match_bg": "#604780",
        "find_current_bg": "#f000ff",
        "syntax": {
            "keyword": "#f000ff",      # Neon Pink
            "function": "#00ffd8",     # Neon Cyan
            "string": "#ffe600",       # Neon Yellow
            "comment": "#685b8c",      # Muted Purple
            "number": "#ff5c00",       # Neon Orange
            "operator": "#00ffd8",     # Neon Cyan
            "name": "#39ff14"          # Neon Green
        }
    },
    "Solarized Dark": {
        "is_dark": True,
        "editor_bg": "#002b36",
        "editor_fg": "#839496",
        "editor_select_bg": "#073642",
        "editor_insert_color": "#93a1a1",
        "current_line_bg": "#073642",
        "line_numbers_bg": "#002b36",
        "line_numbers_fg": "#586e75",
        "line_numbers_current_fg": "#93a1a1",
        "bracket_match_bg": "#073642",
        "bracket_match_fg": "#cb4b16",
        "find_match_bg": "#586e75",
        "find_current_bg": "#2aa198",
        "syntax": {
            "keyword": "#859900",      # Green
            "function": "#268bd2",     # Blue
            "string": "#2aa198",       # Cyan
            "comment": "#586e75",      # Grey
            "number": "#d33682",       # Magenta
            "operator": "#93a1a1",     # Light Grey
            "name": "#b58900"          # Yellow
        }
    },
    "Solarized Light": {
        "is_dark": False,
        "editor_bg": "#fdf6e3",
        "editor_fg": "#657b83",
        "editor_select_bg": "#eee8d5",
        "editor_insert_color": "#586e75",
        "current_line_bg": "#eee8d5",
        "line_numbers_bg": "#fdf6e3",
        "line_numbers_fg": "#93a1a1",
        "line_numbers_current_fg": "#586e75",
        "bracket_match_bg": "#eee8d5",
        "bracket_match_fg": "#cb4b16",
        "find_match_bg": "#93a1a1",
        "find_current_bg": "#2aa198",
        "syntax": {
            "keyword": "#859900",
            "function": "#268bd2",
            "string": "#2aa198",
            "comment": "#93a1a1",
            "number": "#d33682",
            "operator": "#586e75",
            "name": "#b58900"
        }
    },
    "Github Light": {
        "is_dark": False,
        "editor_bg": "#ffffff",
        "editor_fg": "#24292e",
        "editor_select_bg": "#e1e4e6",
        "editor_insert_color": "#0366d6",
        "current_line_bg": "#f6f8fa",
        "line_numbers_bg": "#ffffff",
        "line_numbers_fg": "#cbd3d9",
        "line_numbers_current_fg": "#24292e",
        "bracket_match_bg": "#e1e4e6",
        "bracket_match_fg": "#d73a49",
        "find_match_bg": "#cbd3d9",
        "find_current_bg": "#0366d6",
        "syntax": {
            "keyword": "#d73a49",      # Red
            "function": "#6f42c1",     # Purple
            "string": "#032f62",       # Dark Blue
            "comment": "#6a737d",      # Grey
            "number": "#005cc5",       # Bright Blue
            "operator": "#d73a49",     # Red
            "name": "#e36209"          # Orange
        }
    }
}

class ThemeManager:
    def __init__(self, custom_theme_dir="custom_themes"):
        self.custom_theme_dir = os.path.abspath(custom_theme_dir)
        self.themes = BUILTIN_THEMES.copy()
        self.current_theme_name = "One Dark"
        
        # Load custom themes
        self.load_custom_themes()

    def load_custom_themes(self):
        if not os.path.exists(self.custom_theme_dir):
            try:
                os.makedirs(self.custom_theme_dir)
            except Exception:
                pass
            return

        for filename in os.listdir(self.custom_theme_dir):
            if filename.endswith(".json"):
                path = os.path.join(self.custom_theme_dir, filename)
                try:
                    with open(path, "r") as f:
                        theme_data = json.load(f)
                        # Basic validation
                        required_keys = ["is_dark", "editor_bg", "editor_fg", "editor_select_bg", "editor_insert_color"]
                        if all(k in theme_data for k in required_keys):
                            theme_name = filename[:-5].replace("_", " ").title()
                            self.themes[theme_name] = theme_data
                except Exception as e:
                    print(f"Error loading custom theme {filename}: {e}")

    def save_custom_theme(self, name, data):
        filename = f"{name.lower().replace(' ', '_')}.json"
        path = os.path.join(self.custom_theme_dir, filename)
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            # Add to themes dictionary
            self.themes[name] = data
            return True
        except Exception as e:
            print(f"Error saving custom theme {name}: {e}")
            return False

    def get_theme(self, name=None):
        if name is None:
            name = self.current_theme_name
        return self.themes.get(name, self.themes["One Dark"])

    def get_pygments_style(self, theme_name=None):
        theme = self.get_theme(theme_name)
        syntax = theme.get("syntax", BUILTIN_THEMES["One Dark"]["syntax"])
        
        # Create a dynamic Pygments Style class
        class CustomStyle(Style):
            background_color = theme["editor_bg"]
            highlight_color = theme["current_line_bg"]
            
            # Map Pygments standard tokens to our theme syntax colors
            styles = {
                Keyword: syntax.get("keyword", "#c678dd"),
                Keyword.Namespace: syntax.get("keyword", "#c678dd"),
                Keyword.Type: syntax.get("keyword", "#c678dd"),
                
                Name.Function: syntax.get("function", "#61afef"),
                Name.Class: f"bold {syntax.get('function', '#61afef')}",
                Name.Builtin: syntax.get("keyword", "#c678dd"),
                
                String: syntax.get("string", "#98c379"),
                String.Char: syntax.get("string", "#98c379"),
                
                Comment: f"italic {syntax.get('comment', '#5c6370')}",
                Comment.Preproc: syntax.get("keyword", "#c678dd"),
                
                Number: syntax.get("number", "#d19a66"),
                Operator: syntax.get("operator", "#56b6c2"),
                
                Name: syntax.get("name", "#e06c75"),
                Token.Text: theme["editor_fg"],
                Token.Error: "border:#e06c75"
            }
            
        return CustomStyle
