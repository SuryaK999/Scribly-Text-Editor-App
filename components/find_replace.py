import tkinter as tk
import customtkinter as ctk
import re

class FindReplacePanel(ctk.CTkFrame):
    def __init__(self, parent, editor, theme_manager, close_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.editor = editor
        self.theme_manager = theme_manager
        self.close_callback = close_callback
        
        # State variables
        self.matches = []
        self.current_match_idx = -1
        
        # UI controls vars
        self.find_var = ctk.StringVar(value="")
        self.find_var.trace_add("write", lambda *args: self.perform_search())
        
        self.replace_var = ctk.StringVar(value="")
        
        self.match_case = ctk.BooleanVar(value=False)
        self.use_regex = ctk.BooleanVar(value=False)
        self.whole_word = ctk.BooleanVar(value=False)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        
        # ─── Row 0: Find Input & Controls ───
        find_label = ctk.CTkLabel(self, text="Find:", font=("Segoe UI", 12, "bold"))
        find_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
        
        self.find_entry = ctk.CTkEntry(
            self,
            textvariable=self.find_var,
            placeholder_text="Text to search...",
            font=("Consolas", 12),
            height=28
        )
        self.find_entry.grid(row=0, column=1, padx=5, pady=(10, 5), sticky="ew")
        self.find_entry.bind("<Return>", lambda e: self.next_match())
        
        # Find Navigation Buttons Frame
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.grid(row=0, column=2, padx=5, pady=(10, 5), sticky="w")
        
        self.btn_prev = ctk.CTkButton(
            nav_frame, text="▲", width=30, height=28,
            command=self.prev_match, fg_color="transparent", text_color=("black", "white"),
            hover_color=("gray80", "gray30")
        )
        self.btn_prev.pack(side="left", padx=2)
        
        self.btn_next = ctk.CTkButton(
            nav_frame, text="▼", width=30, height=28,
            command=self.next_match, fg_color="transparent", text_color=("black", "white"),
            hover_color=("gray80", "gray30")
        )
        self.btn_next.pack(side="left", padx=2)
        
        # Status Label (e.g. "2 of 10")
        self.status_lbl = ctk.CTkLabel(self, text="", font=("Segoe UI", 11), text_color="gray")
        self.status_lbl.grid(row=0, column=3, padx=10, pady=(10, 5), sticky="w")
        
        # Close Button
        self.btn_close = ctk.CTkButton(
            self, text="×", width=24, height=24,
            command=self.hide_panel, fg_color="transparent", hover_color=("red2", "red4"),
            text_color=("black", "white"), font=("Segoe UI", 16)
        )
        self.btn_close.grid(row=0, column=4, padx=(5, 10), pady=(10, 5))
        
        # ─── Row 1: Replace Input & Options ───
        replace_label = ctk.CTkLabel(self, text="Replace:", font=("Segoe UI", 12, "bold"))
        replace_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        
        self.replace_entry = ctk.CTkEntry(
            self,
            textvariable=self.replace_var,
            placeholder_text="Replacement text...",
            font=("Consolas", 12),
            height=28
        )
        self.replace_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Replace Actions Frame
        rep_frame = ctk.CTkFrame(self, fg_color="transparent")
        rep_frame.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="w")
        
        self.btn_replace = ctk.CTkButton(
            rep_frame, text="Replace", height=28, width=70,
            command=self.replace_current, font=("Segoe UI", 12)
        )
        self.btn_replace.pack(side="left", padx=2)
        
        self.btn_replace_all = ctk.CTkButton(
            rep_frame, text="Replace All", height=28, width=90,
            command=self.replace_all, font=("Segoe UI", 12)
        )
        self.btn_replace_all.pack(side="left", padx=2)
        
        # ─── Row 2: Search Parameters (Options) ───
        opts_frame = ctk.CTkFrame(self, fg_color="transparent")
        opts_frame.grid(row=2, column=1, columnspan=3, padx=5, pady=(5, 10), sticky="w")
        
        self.chk_case = ctk.CTkCheckBox(
            opts_frame, text="Match Case", variable=self.match_case,
            command=self.perform_search, checkbox_width=18, checkbox_height=18,
            font=("Segoe UI", 11)
        )
        self.chk_case.pack(side="left", padx=(0, 15))
        
        self.chk_regex = ctk.CTkCheckBox(
            opts_frame, text="Use Regex", variable=self.use_regex,
            command=self.perform_search, checkbox_width=18, checkbox_height=18,
            font=("Segoe UI", 11)
        )
        self.chk_regex.pack(side="left", padx=15)
        
        self.chk_word = ctk.CTkCheckBox(
            opts_frame, text="Whole Word", variable=self.whole_word,
            command=self.perform_search, checkbox_width=18, checkbox_height=18,
            font=("Segoe UI", 11)
        )
        self.chk_word.pack(side="left", padx=15)

    def show_panel(self):
        self.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        self.find_entry.focus_set()
        # Highlight existing selection, if any, in the find entry
        try:
            sel_text = self.editor.get("sel.first", "sel.last")
            if sel_text and "\n" not in sel_text:
                self.find_var.set(sel_text)
                self.find_entry.select_range(0, tk.END)
        except Exception:
            pass
        self.perform_search()

    def hide_panel(self):
        self.clear_highlights()
        self.pack_forget()
        self.editor.focus_set()
        if self.close_callback:
            self.close_callback()

    def clear_highlights(self):
        self.editor.tag_remove("search_match", "1.0", "end")
        self.editor.tag_remove("search_current", "1.0", "end")
        self.matches = []
        self.current_match_idx = -1
        self.status_lbl.configure(text="")

    def perform_search(self, keep_index=False):
        # Save previous match index if we want to retain position
        prev_match = None
        if keep_index and 0 <= self.current_match_idx < len(self.matches):
            prev_match = self.matches[self.current_match_idx]
            
        self.clear_highlights()
        pattern = self.find_var.get()
        if not pattern:
            return
            
        nocase = not self.match_case.get()
        regexp = self.use_regex.get()
        
        # Build search patterns considering Whole Word
        if self.whole_word.get():
            if regexp:
                # Add word boundary to regex
                pattern = r"\b" + pattern + r"\b"
            else:
                # Use regex engine for whole word match
                pattern = r"\b" + re.escape(pattern) + r"\b"
                regexp = True
                
        start_pos = "1.0"
        count_var = tk.IntVar()
        
        while True:
            pos = self.editor.search(
                pattern,
                start_pos,
                stopindex="end",
                nocase=nocase,
                regexp=regexp,
                count=count_var
            )
            
            if not pos:
                break
                
            length = count_var.get()
            if length == 0:
                # If regex matched 0 characters (e.g. ^), advance by 1 to prevent infinite loop
                end_pos = self.editor.index(f"{pos} + 1c")
            else:
                end_pos = self.editor.index(f"{pos} + {length}c")
                
            self.matches.append((pos, end_pos))
            self.editor.tag_add("search_match", pos, end_pos)
            
            # Move starting position forward
            start_pos = end_pos
            if self.editor.compare(start_pos, ">=", "end"):
                break
                
        # Lower highlighting tags so they sit below bracket matching & select tags
        self.editor.tag_lower("search_match", "sel")
        
        if self.matches:
            # Re-locate index
            if prev_match and prev_match in self.matches:
                self.current_match_idx = self.matches.index(prev_match)
            else:
                self.current_match_idx = 0
            self.highlight_current()
        else:
            self.status_lbl.configure(text="No matches")

    def highlight_current(self):
        self.editor.tag_remove("search_current", "1.0", "end")
        if not self.matches:
            return
            
        pos, end_pos = self.matches[self.current_match_idx]
        self.editor.tag_add("search_current", pos, end_pos)
        self.editor.tag_raise("search_current", "search_match")
        
        # Scroll editor viewport to show match
        self.editor.see(pos)
        
        # Update labels
        self.status_lbl.configure(text=f"{self.current_match_idx + 1} of {len(self.matches)}")

    def next_match(self):
        if not self.matches:
            return
        self.current_match_idx = (self.current_match_idx + 1) % len(self.matches)
        self.highlight_current()

    def prev_match(self):
        if not self.matches:
            return
        self.current_match_idx = (self.current_match_idx - 1) % len(self.matches)
        self.highlight_current()

    def replace_current(self):
        if not self.matches or self.current_match_idx < 0:
            return
            
        pos, end_pos = self.matches[self.current_match_idx]
        replacement = self.replace_var.get()
        
        # Track replacement scroll position
        self.editor.delete(pos, end_pos)
        self.editor.insert(pos, replacement)
        
        # Re-run search to update match array
        self.perform_search(keep_index=True)
        
    def replace_all(self):
        pattern = self.find_var.get()
        if not pattern:
            return
            
        replacement = self.replace_var.get()
        
        # Re-verify search matches to get accurate indices
        self.perform_search()
        if not self.matches:
            return
            
        # Perform replacements in REVERSE order.
        # This keeps earlier coordinate offsets correct as later ones are deleted/expanded.
        for pos, end_pos in reversed(self.matches):
            self.editor.delete(pos, end_pos)
            self.editor.insert(pos, replacement)
            
        # Re-run search to clear state and show results (which should be 0 matches)
        self.perform_search()
        self.status_lbl.configure(text="Replaced all matches")
