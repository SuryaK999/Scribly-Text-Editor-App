import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os

class FileTree(ctk.CTkFrame):
    def __init__(self, parent, theme_manager, on_file_open_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme_manager = theme_manager
        self.on_file_open = on_file_open_callback
        
        self.root_path = None
        self.nodes = {} # Maps item ID to full path
        
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        # ─── Sidebar Toolbar ───
        self.toolbar = ctk.CTkFrame(self, height=35, fg_color="transparent")
        self.toolbar.pack(fill="x", padx=5, pady=5)
        
        self.lbl_title = ctk.CTkLabel(
            self.toolbar,
            text="Workspace",
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        )
        self.lbl_title.pack(side="left", fill="x", expand=True, padx=5)
        
        self.btn_refresh = ctk.CTkButton(
            self.toolbar,
            text="Refresh",
            width=50,
            height=24,
            font=("Segoe UI", 11),
            fg_color="transparent",
            text_color=("gray30", "gray70"),
            hover_color=("gray85", "gray25"),
            command=self.refresh_tree
        )
        self.btn_refresh.pack(side="right", padx=5)
        
        # ─── Treeview styling & widget ───
        # Create treeview scrollbar
        self.scroll = ctk.CTkScrollbar(self, orientation="vertical")
        self.scroll.pack(side="right", fill="y")
        
        # Configure treeview
        self.tree = ttk.Treeview(
            self,
            show="tree",
            selectmode="browse",
            yscrollcommand=self.scroll.set
        )
        self.tree.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=(0, 5))
        self.scroll.configure(command=self.tree.yview)
        
        # Treeview events
        self.tree.bind("<<TreeviewOpen>>", self.on_node_open)
        self.tree.bind("<Double-1>", self.on_double_click)

    def apply_theme(self):
        theme = self.theme_manager.get_theme()
        bg = theme["editor_bg"]
        fg = theme["editor_fg"]
        select_bg = theme["editor_select_bg"]
        
        # Custom styling of ttk Treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Treeview",
            background=bg,
            foreground=fg,
            fieldbackground=bg,
            rowheight=24,
            borderwidth=0,
            font=("Segoe UI", 11)
        )
        style.map(
            "Treeview",
            background=[("selected", select_bg)],
            foreground=[("selected", fg)],
            focuscolor=[("selected", select_bg)]
        )
        
        # Make the tree scrollbar fit
        self.configure(fg_color=theme["line_numbers_bg"])
        self.toolbar.configure(fg_color=theme["line_numbers_bg"])
        self.lbl_title.configure(text_color=theme["editor_fg"])
        
    def load_directory(self, path):
        if not path or not os.path.exists(path):
            return
            
        self.root_path = os.path.abspath(path)
        self.lbl_title.configure(text=os.path.basename(self.root_path))
        
        # Clear existing items
        self.tree.delete(*self.tree.get_children())
        self.nodes.clear()
        
        # Insert Root Node
        root_node = self.tree.insert("", "end", text=os.path.basename(self.root_path), open=True)
        self.nodes[root_node] = self.root_path
        
        # Populate first level of directories/files
        self.populate_node(root_node, self.root_path)
        
    def populate_node(self, node, path):
        try:
            # List contents
            items = os.listdir(path)
        except Exception:
            return
            
        # Separate directories and files, sort both
        dirs = []
        files = []
        
        for item in items:
            if item.startswith("."):
                continue # Skip hidden folders (git, etc.)
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                dirs.append(item)
            else:
                files.append(item)
                
        dirs.sort(key=str.lower)
        files.sort(key=str.lower)
        
        # Insert directories first
        for d in dirs:
            full_path = os.path.join(path, d)
            child = self.tree.insert(node, "end", text=d, values=("dir",))
            self.nodes[child] = full_path
            
            # Insert dummy item to allow node expansion
            self.tree.insert(child, "end", text="dummy")
            
        # Insert files
        for f in files:
            full_path = os.path.join(path, f)
            child = self.tree.insert(node, "end", text=f, values=("file",))
            self.nodes[child] = full_path

    def on_node_open(self, event):
        node = self.tree.focus()
        if not node:
            return
            
        # Check if the node needs dynamic loading (contains dummy)
        children = self.tree.get_children(node)
        if len(children) == 1 and self.tree.item(children[0], "text") == "dummy":
            # Delete dummy
            self.tree.delete(children[0])
            
            # Load real directories/files
            path = self.nodes[node]
            self.populate_node(node, path)

    def refresh_tree(self):
        if self.root_path:
            self.load_directory(self.root_path)

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
            
        path = self.nodes.get(item)
        if path and os.path.isfile(path):
            if self.on_file_open:
                self.on_file_open(path)
