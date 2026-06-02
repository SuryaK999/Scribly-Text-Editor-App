import os
import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    def __init__(self, parent, theme_manager, **kwargs):
        # Configure frame attributes
        kwargs["height"] = 28
        kwargs["corner_radius"] = 0
        
        super().__init__(parent, **kwargs)
        self.theme_manager = theme_manager
        
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        # Left container
        left_container = ctk.CTkFrame(self, fg_color="transparent")
        left_container.pack(side="left", fill="y", padx=10)
        
        self.lbl_position = ctk.CTkLabel(
            left_container, text="Ln 1, Col 0", font=("Segoe UI", 11)
        )
        self.lbl_position.pack(side="left", padx=10)
        
        self.lbl_stats = ctk.CTkLabel(
            left_container, text="0 chars | 0 words", font=("Segoe UI", 11)
        )
        self.lbl_stats.pack(side="left", padx=10)
        
        self.lbl_zoom = ctk.CTkLabel(
            left_container, text="100%", font=("Segoe UI", 11)
        )
        self.lbl_zoom.pack(side="left", padx=10)
        
        # Right container
        right_container = ctk.CTkFrame(self, fg_color="transparent")
        right_container.pack(side="right", fill="y", padx=10)
        
        self.lbl_theme = ctk.CTkLabel(
            right_container, text="Theme: One Dark", font=("Segoe UI", 11)
        )
        self.lbl_theme.pack(side="right", padx=10)
        
        self.lbl_encoding = ctk.CTkLabel(
            right_container, text="UTF-8", font=("Segoe UI", 11)
        )
        self.lbl_encoding.pack(side="right", padx=10)
        
        self.lbl_filetype = ctk.CTkLabel(
            right_container, text="Plain Text", font=("Segoe UI", 11)
        )
        self.lbl_filetype.pack(side="right", padx=10)
        
    def apply_theme(self):
        theme = self.theme_manager.get_theme()
        bg = theme["line_numbers_bg"]
        fg = theme["line_numbers_fg"]
        
        # Apply visual styles to fit status bar
        self.configure(fg_color=bg)
        
        # Recolor labels
        for label in [self.lbl_position, self.lbl_stats, self.lbl_zoom, self.lbl_theme, self.lbl_encoding, self.lbl_filetype]:
            label.configure(text_color=fg)
            
    def update_status(self, editor, theme_name):
        # 1. Cursor position
        try:
            insert_pos = editor.index("insert")
            line, col = insert_pos.split(".")
            self.lbl_position.configure(text=f"Ln {line}, Col {col}")
        except Exception:
            pass
            
        # 2. Text Statistics
        try:
            content = editor.get("1.0", "end-1c")
            char_count = len(content)
            word_count = len(content.split()) if content.strip() else 0
            self.lbl_stats.configure(text=f"{char_count} chars | {word_count} words")
        except Exception:
            pass
            
        # 3. Zoom
        try:
            self.lbl_zoom.configure(text=f"Zoom: {editor.get_zoom_percent()}%")
        except Exception:
            pass
            
        # 4. File Type
        try:
            if editor.lexer:
                self.lbl_filetype.configure(text=editor.lexer.name)
            else:
                # Guess from file extension if no lexer
                if editor.file_path:
                    _, ext = os.path.splitext(editor.file_path)
                    ext = ext.lstrip(".").upper()
                    self.lbl_filetype.configure(text=f"{ext} File" if ext else "Plain Text")
                else:
                    self.lbl_filetype.configure(text="Plain Text")
        except Exception:
            self.lbl_filetype.configure(text="Plain Text")
            
        # 5. Theme
        self.lbl_theme.configure(text=f"Theme: {theme_name}")
