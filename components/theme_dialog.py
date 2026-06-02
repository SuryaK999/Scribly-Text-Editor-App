import tkinter as tk
from tkinter import colorchooser, messagebox
import customtkinter as ctk
import os
import sys

class ThemeDialog(ctk.CTkToplevel):
    def __init__(self, parent, theme_manager, on_save_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme_manager = theme_manager
        self.on_save_callback = on_save_callback
        
        self.title("Theme Creator")
        self.geometry("450x620")
        self.resizable(False, False)
        
        # Keep window on top and grab focus
        self.transient(parent)
        self.grab_set()
        
        # Set the Scribly app icon on this dialog window
        self._load_dialog_icon()
        
        # Load currently active theme colors as initial values
        current_theme = self.theme_manager.get_theme()
        syntax = current_theme.get("syntax", {})
        
        self.theme_name_var = ctk.StringVar(value="My Custom Theme")
        self.is_dark_var = ctk.BooleanVar(value=current_theme.get("is_dark", True))
        
        # Theme data storage
        self.colors = {
            "editor_bg": current_theme.get("editor_bg", "#282c34"),
            "editor_fg": current_theme.get("editor_fg", "#abb2bf"),
            "editor_select_bg": current_theme.get("editor_select_bg", "#3e4451"),
            "editor_insert_color": current_theme.get("editor_insert_color", "#528bff"),
            "current_line_bg": current_theme.get("current_line_bg", "#2c313c"),
            "line_numbers_bg": current_theme.get("line_numbers_bg", "#282c34"),
            "line_numbers_fg": current_theme.get("line_numbers_fg", "#4b5263"),
            
            # Syntax styles
            "syntax_keyword": syntax.get("keyword", "#c678dd"),
            "syntax_function": syntax.get("function", "#61afef"),
            "syntax_string": syntax.get("string", "#98c379"),
            "syntax_comment": syntax.get("comment", "#5c6370")
        }
        
        self.color_buttons = {}
        self.setup_ui()
    
    def _load_dialog_icon(self):
        """Load the Scribly app icon on this dialog window."""
        try:
            icon_png_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.png")
            icon_ico_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.ico")
            
            if os.path.exists(icon_png_path):
                from PIL import Image, ImageTk
                img = Image.open(icon_png_path)
                sizes = [16, 32, 48, 64, 128, 256]
                photos = [ImageTk.PhotoImage(img.resize((s, s), Image.Resampling.LANCZOS)) for s in sizes]
                self.iconphoto(False, *photos)
                self._icon_photos = photos  # prevent GC
                
            if sys.platform.startswith("win") and os.path.exists(icon_ico_path):
                self.after(100, lambda: self.iconbitmap(icon_ico_path))
        except Exception:
            pass
        
    def setup_ui(self):
        # Master padding frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Title Label
        title_lbl = ctk.CTkLabel(main_frame, text="Create Custom Theme", font=("Segoe UI", 16, "bold"))
        title_lbl.pack(pady=(10, 15))
        
        # Theme Name input
        name_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=10, pady=5)
        
        name_lbl = ctk.CTkLabel(name_frame, text="Theme Name:", font=("Segoe UI", 12))
        name_lbl.pack(side="left", padx=5)
        
        name_entry = ctk.CTkEntry(name_frame, textvariable=self.theme_name_var, width=200)
        name_entry.pack(side="right", padx=5, expand=True, fill="x")
        
        # Mode switch (Light/Dark)
        mode_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        mode_frame.pack(fill="x", padx=10, pady=5)
        
        mode_lbl = ctk.CTkLabel(mode_frame, text="Base Mode:", font=("Segoe UI", 12))
        mode_lbl.pack(side="left", padx=5)
        
        mode_switch = ctk.CTkSwitch(mode_frame, text="Dark Mode UI", variable=self.is_dark_var)
        mode_switch.pack(side="right", padx=5)
        
        # Color Grid container
        grid_frame = ctk.CTkFrame(main_frame)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=15)
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        
        labels_and_keys = [
            ("Editor Background", "editor_bg"),
            ("Text Color (Foreground)", "editor_fg"),
            ("Selection Highlight", "editor_select_bg"),
            ("Cursor / Insert Mark", "editor_insert_color"),
            ("Active Line Highlight", "current_line_bg"),
            ("Line Numbers Background", "line_numbers_bg"),
            ("Line Numbers Text Color", "line_numbers_fg"),
            ("Syntax: Keywords", "syntax_keyword"),
            ("Syntax: Functions/Classes", "syntax_function"),
            ("Syntax: Strings", "syntax_string"),
            ("Syntax: Comments", "syntax_comment")
        ]
        
        for idx, (label_text, key) in enumerate(labels_and_keys):
            row = idx
            
            lbl = ctk.CTkLabel(grid_frame, text=label_text, font=("Segoe UI", 11))
            lbl.grid(row=row, column=0, padx=10, pady=4, sticky="w")
            
            # Color indicator button
            current_hex = self.colors[key]
            btn = ctk.CTkButton(
                grid_frame,
                text=current_hex,
                fg_color=current_hex,
                text_color=self.get_contrasting_text_color(current_hex),
                height=22,
                font=("Consolas", 11),
                border_width=1,
                border_color="gray",
                command=lambda k=key: self.choose_color(k)
            )
            btn.grid(row=row, column=1, padx=10, pady=4, sticky="ew")
            self.color_buttons[key] = btn
            
        # Action Buttons
        act_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        act_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.btn_cancel = ctk.CTkButton(
            act_frame, text="Cancel", fg_color="transparent", border_width=1,
            text_color=("black", "white"), command=self.destroy, width=100
        )
        self.btn_cancel.pack(side="left", padx=5)
        
        self.btn_save = ctk.CTkButton(
            act_frame, text="Save Theme", command=self.save_theme, width=150
        )
        self.btn_save.pack(side="right", padx=5)
        
    def get_contrasting_text_color(self, hex_color):
        # Calculate luminance to decide black or white text
        try:
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return "#000000" if luminance > 0.5 else "#ffffff"
        except Exception:
            return "#ffffff"
            
    def choose_color(self, key):
        current_color = self.colors[key]
        # Open standard OS color chooser
        _, hex_color = colorchooser.askcolor(initialcolor=current_color, title=f"Select Color for {key}")
        if hex_color:
            self.colors[key] = hex_color
            btn = self.color_buttons[key]
            btn.configure(
                text=hex_color,
                fg_color=hex_color,
                text_color=self.get_contrasting_text_color(hex_color)
            )
            
    def save_theme(self):
        name = self.theme_name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Theme name cannot be empty.")
            return
            
        if name in self.theme_manager.themes and name in ["One Dark", "Monokai", "Cyberpunk", "Solarized Dark", "Solarized Light", "Github Light"]:
            messagebox.showerror("Error", "Cannot overwrite built-in themes.")
            return
            
        # Structure the theme data
        theme_data = {
            "is_dark": self.is_dark_var.get(),
            "editor_bg": self.colors["editor_bg"],
            "editor_fg": self.colors["editor_fg"],
            "editor_select_bg": self.colors["editor_select_bg"],
            "editor_insert_color": self.colors["editor_insert_color"],
            "current_line_bg": self.colors["current_line_bg"],
            "line_numbers_bg": self.colors["line_numbers_bg"],
            "line_numbers_fg": self.colors["line_numbers_fg"],
            "line_numbers_current_fg": self.colors["editor_fg"],
            
            # Use editor selection color for bracket highlight background, and foreground for text
            "bracket_match_bg": self.colors["editor_select_bg"],
            "bracket_match_fg": self.colors["syntax_keyword"],
            
            # Match search highlights
            "find_match_bg": self.colors["line_numbers_fg"],
            "find_current_bg": self.colors["syntax_function"],
            
            "syntax": {
                "keyword": self.colors["syntax_keyword"],
                "function": self.colors["syntax_function"],
                "string": self.colors["syntax_string"],
                "comment": self.colors["syntax_comment"],
                "number": self.colors["syntax_keyword"],       # Fallbacks
                "operator": self.colors["editor_fg"],
                "name": self.colors["syntax_function"]
            }
        }
        
        success = self.theme_manager.save_custom_theme(name, theme_data)
        if success:
            if self.on_save_callback:
                self.on_save_callback(name)
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to save custom theme JSON file.")
