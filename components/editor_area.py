import tkinter as tk
from tkinter import font
import os
import re
from pygments import lex
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
from pygments.util import ClassNotFound

class EditorArea(tk.Text):
    def __init__(self, parent, theme_manager, status_callback=None, **kwargs):
        self.theme_manager = theme_manager
        self.status_callback = status_callback
        
        # Font settings
        self.font_family = "Consolas"
        self.base_font_size = 12
        self.current_font_size = self.base_font_size
        self.custom_font = font.Font(family=self.font_family, size=self.current_font_size)
        
        # Configure text widget arguments
        kwargs["font"] = self.custom_font
        kwargs["undo"] = True
        kwargs["maxundo"] = 50
        kwargs["autoseparators"] = True
        kwargs["wrap"] = tk.WORD
        
        super().__init__(parent, **kwargs)
        
        # Current file path associated with the editor
        self.file_path = None
        self.lexer = None
        self._highlight_job = None
        
        # Proxy interceptor for scroll and change notifications
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        
        # Setup tags
        self.setup_tags()
        
        # Bindings
        self.bind("<<Selection>>", self.on_cursor_or_selection)
        self.bind("<KeyRelease>", self.on_key_release)
        self.bind("<ButtonRelease-1>", self.on_cursor_or_selection)
        
        # Auto-closing and bracket bindings
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<BackSpace>", self.on_backspace)
        self.bind("<Return>", self.on_return)
        
        # Zoom bindings
        self.bind("<Control-MouseWheel>", self.on_zoom_windows)
        self.bind("<Control-KeyPress-plus>", self.zoom_in)
        self.bind("<Control-KeyPress-equal>", self.zoom_in)
        self.bind("<Control-KeyPress-minus>", self.zoom_out)
        
        # Apply initial theme colors
        self.apply_theme()
        
    def setup_tags(self):
        # Configure highlight tags for syntax
        # Pygments token tag names are mapped to specific colors in theme
        self.tag_configure("Token.Keyword", font=(self.font_family, self.current_font_size, "bold"))
        self.tag_configure("Token.Name.Function", font=(self.font_family, self.current_font_size))
        self.tag_configure("Token.Name.Class", font=(self.font_family, self.current_font_size, "bold"))
        self.tag_configure("Token.String", font=(self.font_family, self.current_font_size))
        self.tag_configure("Token.Comment", font=(self.font_family, self.current_font_size, "italic"))
        self.tag_configure("Token.Number", font=(self.font_family, self.current_font_size))
        self.tag_configure("Token.Operator", font=(self.font_family, self.current_font_size))
        self.tag_configure("Token.Name", font=(self.font_family, self.current_font_size))
        
        # Selection, Search and Bracket highlights
        self.tag_configure("current_line", background="#2c313c")
        # lower the priority of current line tag so search and bracket highlights show over it
        self.tag_lower("current_line")
        
        self.tag_configure("bracket_match", background="#3e4451", relief="raised", borderwidth=1)
        self.tag_configure("search_match", background="#4b5263")
        self.tag_configure("search_current", background="#61afef", foreground="#ffffff")
        
    def _proxy(self, *args):
        # Prevent errors during widget destruction
        try:
            result = self.tk.call(self._orig, *args)
        except Exception:
            return ""
        
        # Generate custom event on changes or scrolls
        if args[0] in ("insert", "delete", "replace") or args[0] in ("yview", "xview"):
            self.event_generate("<<TextModified>>", when="tail")
            
        # Trigger highlighting on modification commands
        if args[0] in ("insert", "delete", "replace"):
            self.trigger_highlighting()
            
        return result

    def set_file_path(self, path):
        self.file_path = path
        self.update_lexer()
        self.trigger_highlighting()
        
    def update_lexer(self):
        if self.file_path:
            try:
                self.lexer = get_lexer_for_filename(self.file_path)
            except ClassNotFound:
                # Fallback to python lexer if file is unknown but contains code keywords, or plain text
                ext = os.path.splitext(self.file_path)[1].lower()
                if ext in (".py", ".pyw"):
                    self.lexer = get_lexer_by_name("python")
                else:
                    self.lexer = None
        else:
            self.lexer = None

    def apply_theme(self):
        theme = self.theme_manager.get_theme()
        
        # Apply editor base colors
        self.configure(
            bg=theme["editor_bg"],
            fg=theme["editor_fg"],
            selectbackground=theme["editor_select_bg"],
            insertbackground=theme["editor_insert_color"]
        )
        
        # Apply special highlights
        self.tag_configure("current_line", background=theme["current_line_bg"])
        self.tag_configure("bracket_match", background=theme["bracket_match_bg"], foreground=theme["bracket_match_fg"])
        self.tag_configure("search_match", background=theme["find_match_bg"])
        self.tag_configure("search_current", background=theme["find_current_bg"], foreground=theme["editor_bg"])
        
        # Syntax styles configurations
        syntax = theme.get("syntax", {})
        self.tag_configure("Token.Keyword", foreground=syntax.get("keyword", "#c678dd"))
        self.tag_configure("Token.Name.Function", foreground=syntax.get("function", "#61afef"))
        self.tag_configure("Token.Name.Class", foreground=syntax.get("function", "#61afef"))
        self.tag_configure("Token.String", foreground=syntax.get("string", "#98c379"))
        self.tag_configure("Token.Comment", foreground=syntax.get("comment", "#5c6370"))
        self.tag_configure("Token.Number", foreground=syntax.get("number", "#d19a66"))
        self.tag_configure("Token.Operator", foreground=syntax.get("operator", "#56b6c2"))
        self.tag_configure("Token.Name", foreground=syntax.get("name", "#e06c75"))
        
        # Refresh highlighting
        self.trigger_highlighting()
        
    def trigger_highlighting(self):
        if self._highlight_job:
            self.after_cancel(self._highlight_job)
        self._highlight_job = self.after(100, self.perform_highlighting)

    def perform_highlighting(self):
        if not self.lexer:
            # Clear all syntax tags
            for tag in ["Token.Keyword", "Token.Name.Function", "Token.Name.Class", "Token.String", "Token.Comment", "Token.Number", "Token.Operator", "Token.Name"]:
                self.tag_remove(tag, "1.0", "end")
            return
            
        content = self.get("1.0", "end-1c")
        
        # Clear existing syntax tags
        for tag in ["Token.Keyword", "Token.Name.Function", "Token.Name.Class", "Token.String", "Token.Comment", "Token.Number", "Token.Operator", "Token.Name"]:
            self.tag_remove(tag, "1.0", "end")
            
        tokens = list(lex(content, self.lexer))
        
        # Track line and column in Tkinter terms (1-based lines, 0-based columns)
        line = 1
        col = 0
        
        for token_type, value in tokens:
            token_len = len(value)
            
            # Map deep token types to our base tags
            tag_name = None
            str_token = str(token_type)
            
            if "Keyword" in str_token:
                tag_name = "Token.Keyword"
            elif "Name.Function" in str_token:
                tag_name = "Token.Name.Function"
            elif "Name.Class" in str_token:
                tag_name = "Token.Name.Class"
            elif "String" in str_token:
                tag_name = "Token.String"
            elif "Comment" in str_token:
                tag_name = "Token.Comment"
            elif "Number" in str_token:
                tag_name = "Token.Number"
            elif "Operator" in str_token:
                tag_name = "Token.Operator"
            elif "Name" in str_token:
                tag_name = "Token.Name"
                
            start_index = f"{line}.{col}"
            
            # Split the value by newlines to update line and column pointers correctly
            lines_in_value = value.split("\n")
            if len(lines_in_value) > 1:
                line += len(lines_in_value) - 1
                col = len(lines_in_value[-1])
            else:
                col += token_len
                
            end_index = f"{line}.{col}"
            
            if tag_name:
                self.tag_add(tag_name, start_index, end_index)

    def on_key_release(self, event):
        if event.keysym in ("Left", "Right", "Up", "Down", "Prior", "Next"):
            self.on_cursor_or_selection()

    def on_cursor_or_selection(self, event=None):
        self.highlight_current_line()
        self.perform_bracket_matching()
        if self.status_callback:
            self.status_callback()

    def highlight_current_line(self):
        self.tag_remove("current_line", "1.0", "end")
        current_line_idx = self.index("insert linestart")
        next_line_idx = self.index("insert lineend + 1c")
        self.tag_add("current_line", current_line_idx, next_line_idx)
        # Ensure it stays behind everything else
        self.tag_lower("current_line")

    def perform_bracket_matching(self):
        self.tag_remove("bracket_match", "1.0", "end")
        
        curr_pos = self.index("insert")
        
        # Check character to the left
        char_left = ""
        left_pos = self.index(f"{curr_pos} - 1c")
        if self.compare(left_pos, ">=", "1.0"):
            char_left = self.get(left_pos)
            
        # Check character to the right
        char_right = ""
        right_pos = curr_pos
        if self.compare(right_pos, "<", "end-1c"):
            char_right = self.get(right_pos)
            
        brackets = {
            "(": (")", 1), "[": ("]", 1), "{": ("}", 1),
            ")": ("(", -1), "]": ("[", -1), "}": ("{", -1)
        }
        
        target_char = None
        target_pos = None
        
        if char_right in brackets:
            target_char = char_right
            target_pos = right_pos
        elif char_left in brackets:
            target_char = char_left
            target_pos = left_pos
            
        if not target_char:
            return
            
        matching_char, direction = brackets[target_char]
        depth = 0
        search_pos = target_pos
        
        while True:
            if direction > 0:
                search_pos = self.index(f"{search_pos} + 1c")
                if self.compare(search_pos, ">=", "end-1c"):
                    break
            else:
                search_pos = self.index(f"{search_pos} - 1c")
                if self.compare(search_pos, "<", "1.0"):
                    break
                    
            c = self.get(search_pos)
            if c == target_char:
                depth += 1
            elif c == matching_char:
                if depth == 0:
                    # Found match!
                    self.tag_add("bracket_match", target_pos, f"{target_pos} + 1c")
                    self.tag_add("bracket_match", search_pos, f"{search_pos} + 1c")
                    break
                else:
                    depth -= 1

    def on_key_press(self, event):
        # Auto-closing quotes and brackets
        char = event.char
        if not char:
            return
            
        pairs = {"(": ")", "[": "]", "{": "}", '"': '"', "'": "'"}
        
        if char in pairs:
            closing = pairs[char]
            
            # If quotes, check if cursor is already preceding a quote to step over
            if char in ('"', "'"):
                curr_char = self.get("insert")
                if curr_char == char:
                    # Just step over
                    self.mark_set("insert", "insert + 1c")
                    return "break"
            
            # Insert pair
            self.insert("insert", char + closing)
            self.mark_set("insert", "insert - 1c")
            return "break"
            
        elif char in (")", "]", "}"):
            curr_char = self.get("insert")
            if curr_char == char:
                # Step over closing bracket
                self.mark_set("insert", "insert + 1c")
                return "break"

    def on_backspace(self, event):
        # Delete bracket pairs if they are side-by-side
        curr_pos = self.index("insert")
        left_pos = self.index(f"{curr_pos} - 1c")
        
        if self.compare(left_pos, ">=", "1.0"):
            char_left = self.get(left_pos)
            char_right = self.get(curr_pos)
            
            pairs = ["()", "[]", "{}", '""', "''"]
            if char_left + char_right in pairs:
                self.delete(left_pos, f"{curr_pos} + 1c")
                return "break"

    def on_return(self, event):
        # Auto-indentation
        curr_line = self.get("insert linestart", "insert")
        
        # Extract leading whitespace
        indent_match = re.match(r"^(\s*)", curr_line)
        indent = indent_match.group(1) if indent_match else ""
        
        # Check if the line ends with a colon or open brace/bracket
        stripped_line = curr_line.strip()
        extra_indent = ""
        if stripped_line.endswith(":") or stripped_line.endswith("{") or stripped_line.endswith("[") or stripped_line.endswith("("):
            extra_indent = "    " # 4 spaces
            
        self.insert("insert", "\n" + indent + extra_indent)
        # Scroll to ensure cursor is visible
        self.see("insert")
        return "break"

    # Font Zoom Control
    def on_zoom_windows(self, event):
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        return "break"
        
    def zoom_in(self, event=None):
        if self.current_font_size < 30:
            self.current_font_size += 1
            self.update_font()
        return "break"
        
    def zoom_out(self, event=None):
        if self.current_font_size > 8:
            self.current_font_size -= 1
            self.update_font()
        return "break"
        
    def update_font(self):
        self.custom_font.configure(size=self.current_font_size)
        # Update tag font configurations to reflect new size
        self.setup_tags()
        if self.status_callback:
            self.status_callback()
            
    def get_zoom_percent(self):
        return int((self.current_font_size / self.base_font_size) * 100)
