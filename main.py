import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
import os
import sys

# Windows Taskbar grouping fix (Must be called before Tkinter window initialization)
if sys.platform.startswith("win"):
    try:
        import ctypes
        myappid = 'scribly.texteditor.app.v4'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

# Import custom components
from theme_manager import ThemeManager
from components.editor_area import EditorArea
from components.line_numbers import LineNumbers
from components.find_replace import FindReplacePanel
from components.theme_dialog import ThemeDialog
from components.file_tree import FileTree
from components.status_bar import StatusBar

# Initialize CustomTkinter appearance settings
ctk.set_default_color_theme("blue")

class TextEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure app state
        self.theme_manager = ThemeManager()
        self.current_theme_name = self.theme_manager.current_theme_name
        self.open_file_path = None
        self.is_sidebar_visible = False # Hidden by default for a clean, minimal look
        
        # Set Window Attributes
        self.title("Untitled - Scribly")
        self.geometry("950x600")
        self.minsize(600, 400)
        
        # Load cross-platform window icon
        self.load_icon()
        
        # Apply initial system theme
        theme = self.theme_manager.get_theme()
        ctk.set_appearance_mode("dark" if theme["is_dark"] else "light")
        
        self.setup_ui()
        self.setup_menus()
        self.bind_shortcuts()
        
        # Load active directory in the sidebar if available
        self.file_tree.load_directory("d:/python-experiment-apps/Text Editor")
        
        # Set up closing callback to prompt saving changes
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def load_icon(self):
        try:
            icon_png_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
            icon_ico_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            
            # Load multiple sizes of PNG for high-DPI scaling support (Linux/macOS/Windows)
            if os.path.exists(icon_png_path):
                from PIL import Image, ImageTk
                img = Image.open(icon_png_path)
                
                # Generate multiple resolutions for Tkinter iconphoto (Tkinter selects best resolution automatically)
                sizes = [16, 32, 48, 64, 128, 256]
                photos = []
                for s in sizes:
                    resized_img = img.resize((s, s), Image.Resampling.LANCZOS)
                    photos.append(ImageTk.PhotoImage(resized_img))
                
                # Set all photos as the icon (Tkinter selects best resolution)
                self.iconphoto(False, *photos)
                # Keep references to avoid garbage collection
                self._icon_photos = photos
                
            # If on Windows, load the .ico file for native title bar/taskbar window icon
            if sys.platform.startswith("win") and os.path.exists(icon_ico_path):
                self.after(200, lambda: self.iconbitmap(icon_ico_path))
        except Exception as e:
            print(f"Error loading icon: {e}")
        
    def setup_ui(self):
        # ─── Master Grid / Frame Layout ───
        # Main layout: Toolbar (top), central workspace (middle), Status Bar (bottom)
        
        # 1. Toolbar
        self.toolbar_frame = ctk.CTkFrame(self, height=35, corner_radius=0)
        self.toolbar_frame.pack(side="top", fill="x")
        self.setup_toolbar()
        
        # Horizontal Separator (Thin 1px line)
        self.sep = ctk.CTkFrame(self, height=1)
        self.sep.pack(side="top", fill="x")
        
        # 2. Main Workspace (Contains Sidebar & Editor Area)
        self.workspace_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace_frame.pack(side="top", fill="both", expand=True)
        
        # Sidebar Frame (Collapsible) - Hidden on startup
        self.sidebar_frame = ctk.CTkFrame(self.workspace_frame, width=220, corner_radius=0)
        self.sidebar_frame.pack_propagate(False) # Keep width fixed
        
        # File Tree sidebar
        self.file_tree = FileTree(
            self.sidebar_frame,
            self.theme_manager,
            on_file_open_callback=self.open_file
        )
        self.file_tree.pack(fill="both", expand=True)
        
        # Splitter bar (Simple styling 1px separator) - Hidden on startup
        self.splitter = ctk.CTkFrame(self.workspace_frame, width=1)
        
        # Editor Container (Holds Editor, Line Numbers and Scrollbar)
        self.editor_container = ctk.CTkFrame(self.workspace_frame, fg_color="transparent")
        self.editor_container.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        self.editor_scrollbar = ctk.CTkScrollbar(self.editor_container, orientation="vertical")
        self.editor_scrollbar.pack(side="right", fill="y")
        
        # The main Editor widget
        self.editor = EditorArea(
            self.editor_container,
            self.theme_manager,
            status_callback=self.on_editor_event,
            undo=True
        )
        self.editor.pack(side="right", fill="both", expand=True)
        self.editor.configure(yscrollcommand=self.editor_scrollbar.set)
        self.editor_scrollbar.configure(command=self.editor.yview)
        
        # Real-time line numbers sidebar
        self.line_numbers = LineNumbers(self.editor_container, self.editor, self.theme_manager)
        self.line_numbers.pack(side="left", fill="y")
        
        # Bind double check on edit-modified
        self.editor.bind("<<Modified>>", self.on_modified_flag_change)
        
        # 3. Find & Replace Panel (Hidden by default, pack at bottom)
        self.find_replace = FindReplacePanel(
            self,
            self.editor,
            self.theme_manager,
            close_callback=self.on_find_replace_close
        )
        # Keeps panel at bottom above status bar
        
        # 4. Status Bar
        self.status_bar = StatusBar(self, self.theme_manager)
        self.status_bar.pack(side="bottom", fill="x")
        
        # Populate initial status bar
        self.on_editor_event()
        
    def setup_toolbar(self):
        # Professional flat text buttons
        actions = [
            ("New", self.new_file, "New File (Ctrl+N)"),
            ("Open", lambda: self.open_file(), "Open File (Ctrl+O)"),
            ("Save", self.save_file, "Save File (Ctrl+S)"),
            ("Find", self.toggle_find_replace, "Find & Replace (Ctrl+F)"),
            ("Sidebar", self.toggle_sidebar, "Toggle Sidebar (Ctrl+B)")
        ]
        
        for text, cmd, tooltip in actions:
            btn = ctk.CTkButton(
                self.toolbar_frame,
                text=text,
                width=60,
                height=26,
                command=cmd,
                fg_color="transparent",
                text_color=("gray30", "gray70"),
                hover_color=("gray85", "gray25"),
                font=("Segoe UI", 11),
                corner_radius=4
            )
            btn.pack(side="left", padx=2, pady=4)
            
        # Theme Picker Dropdown
        theme_lbl = ctk.CTkLabel(self.toolbar_frame, text="Theme:", font=("Segoe UI", 11))
        theme_lbl.pack(side="left", padx=(15, 5))
        
        self.theme_selector = ctk.CTkOptionMenu(
            self.toolbar_frame,
            values=list(self.theme_manager.themes.keys()),
            command=self.change_theme,
            width=120,
            height=26,
            font=("Segoe UI", 11)
        )
        self.theme_selector.set(self.current_theme_name)
        self.theme_selector.pack(side="left", padx=5)
        
        # Custom Theme Creator Button
        self.btn_new_theme = ctk.CTkButton(
            self.toolbar_frame,
            text="+ Custom Theme",
            width=110,
            height=26,
            command=self.open_theme_creator,
            font=("Segoe UI", 11),
            fg_color="transparent",
            text_color=("gray30", "gray70"),
            hover_color=("gray85", "gray25"),
            border_width=1,
            border_color=("gray80", "gray30")
        )
        self.btn_new_theme.pack(side="left", padx=10)
        
    def setup_menus(self):
        # Create standard OS menus (styled where supported)
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New File", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open File...", command=lambda: self.open_file(), accelerator="Ctrl+O")
        self.file_menu.add_command(label="Open Workspace Folder...", command=self.open_folder)
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=lambda: self.editor.event_generate("<<Undo>>"), accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=lambda: self.editor.event_generate("<<Redo>>"), accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.editor.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=lambda: self.editor.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=lambda: self.editor.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find / Replace...", command=self.toggle_find_replace, accelerator="Ctrl+F")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # View Menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Toggle Workspace Sidebar", command=self.toggle_sidebar, accelerator="Ctrl+B")
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Zoom In", command=self.editor.zoom_in, accelerator="Ctrl++")
        self.view_menu.add_command(label="Zoom Out", command=self.editor.zoom_out, accelerator="Ctrl+-")
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        
    def bind_shortcuts(self):
        # Global bindings
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-S>", lambda e: self.save_file_as()) # Ctrl+Shift+S
        self.bind("<Control-f>", lambda e: self.toggle_find_replace())
        self.bind("<Control-b>", lambda e: self.toggle_sidebar())
        self.bind("<Control-q>", lambda e: self.on_closing())
        self.bind("<Control-w>", lambda e: self.on_closing())
        
        # Standard Redo mapping on windows
        self.bind("<Control-y>", lambda e: self.editor.event_generate("<<Redo>>"))

    def change_theme(self, theme_name):
        self.current_theme_name = theme_name
        self.theme_manager.current_theme_name = theme_name
        self.theme_selector.set(theme_name)
        
        theme = self.theme_manager.get_theme(theme_name)
        
        # Update CustomTkinter root mode
        ctk.set_appearance_mode("dark" if theme["is_dark"] else "light")
        
        # Recursively update app widgets styling
        self.toolbar_frame.configure(fg_color=theme["editor_bg"])
        self.sep.configure(fg_color=("gray75", "gray25") if theme["is_dark"] else ("gray85", "gray15"))
        self.sidebar_frame.configure(fg_color=theme["line_numbers_bg"])
        self.splitter.configure(fg_color=("gray75", "gray25") if theme["is_dark"] else ("gray85", "gray15"))
        
        # Propagate changes to component classes
        self.editor.apply_theme()
        self.line_numbers.redraw()
        self.file_tree.apply_theme()
        self.status_bar.apply_theme()
        
        # Recolor standard OS menu if OS supports it
        try:
            self.menu_bar.configure(
                bg=theme["line_numbers_bg"],
                fg=theme["editor_fg"],
                activebackground=theme["editor_select_bg"],
                activeforeground=theme["editor_fg"]
            )
        except Exception:
            pass
            
        self.on_editor_event()

    def open_theme_creator(self):
        # Open custom Theme Dialog as modal
        ThemeDialog(self, self.theme_manager, on_save_callback=self.on_custom_theme_saved)

    def on_custom_theme_saved(self, new_theme_name):
        # Refresh picker menu with the new custom theme
        self.theme_selector.configure(values=list(self.theme_manager.themes.keys()))
        self.change_theme(new_theme_name)

    def on_editor_event(self):
        # Dispatches UI state updates to status bar
        self.status_bar.update_status(self.editor, self.current_theme_name)
        
    def on_modified_flag_change(self, event=None):
        if self.editor.edit_modified():
            self.update_title(dirty=True)
            
    def update_title(self, dirty=False):
        filename = os.path.basename(self.open_file_path) if self.open_file_path else "Untitled"
        dirty_marker = " •" if dirty else ""
        self.title(f"{filename}{dirty_marker} - Scribly")

    def toggle_sidebar(self):
        if self.is_sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.splitter.pack_forget()
            self.is_sidebar_visible = False
        else:
            # Show sidebar again on the left
            self.sidebar_frame.pack(side="left", fill="y")
            self.splitter.pack(side="left", fill="y")
            # Pull editor components behind sidebar elements
            self.sidebar_frame.pack_configure(before=self.splitter)
            self.splitter.pack_configure(before=self.editor_container)
            self.is_sidebar_visible = True

    def toggle_find_replace(self):
        # If open, hide. Else, show.
        if self.find_replace.winfo_ismapped():
            self.find_replace.hide_panel()
        else:
            self.find_replace.show_panel()
            
    def on_find_replace_close(self):
        # Ensure focus returns to editor
        self.editor.focus_set()

    # ─── File operations ───
    
    def check_save_changes(self):
        # Check if editor content is dirty
        if self.editor.edit_modified():
            filename = os.path.basename(self.open_file_path) if self.open_file_path else "Untitled"
            res = messagebox.askyesnocancel(
                "Unsaved Changes",
                f"Do you want to save changes to {filename}?"
            )
            if res is True: # Yes
                self.save_file()
                return not self.editor.edit_modified() # True if saved successfully
            elif res is False: # No
                return True # Proceed without saving
            else: # Cancel
                return False
        return True # Safe to proceed
        
    def new_file(self):
        if not self.check_save_changes():
            return
            
        self.editor.delete("1.0", "end")
        self.editor.edit_modified(False)
        self.open_file_path = None
        self.editor.set_file_path(None)
        
        self.update_title(dirty=False)
        self.on_editor_event()
        self.line_numbers.redraw()

    def open_file(self, path=None):
        if not self.check_save_changes():
            return
            
        if not path:
            path = filedialog.askopenfilename(
                filetypes=[
                    ("All Files", "*.*"),
                    ("Python Files", "*.py;*.pyw"),
                    ("Text Files", "*.txt"),
                    ("Markdown Files", "*.md"),
                    ("JSON Files", "*.json"),
                    ("Web Files", "*.html;*.css;*.js")
                ]
            )
            
        if not path:
            return
            
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
                
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", content)
            
            # Setup path and lexer
            self.open_file_path = path
            self.editor.set_file_path(path)
            
            # Reset modified flag
            self.editor.edit_modified(False)
            self.update_title(dirty=False)
            
            # Clear text highlights if find panel was open
            self.find_replace.clear_highlights()
            
            # Force redraw
            self.line_numbers.redraw()
            self.on_editor_event()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")

    def save_file(self):
        if not self.open_file_path:
            return self.save_file_as()
            
        try:
            content = self.editor.get("1.0", "end-1c")
            with open(self.open_file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            self.editor.edit_modified(False)
            self.update_title(dirty=False)
            self.on_editor_event()
            self.file_tree.refresh_tree()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")
            return False

    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("Markdown Files", "*.md"),
                ("JSON Files", "*.json"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("All Files", "*.*")
            ]
        )
        if not path:
            return False
            
        self.open_file_path = path
        self.editor.set_file_path(path)
        return self.save_file()

    def open_folder(self):
        path = filedialog.askdirectory(title="Select Workspace Directory")
        if path:
            self.file_tree.load_directory(path)

    def on_closing(self, event=None):
        if self.check_save_changes():
            self.destroy()
            sys.exit(0)

if __name__ == "__main__":
    app = TextEditorApp()
    app.mainloop()
