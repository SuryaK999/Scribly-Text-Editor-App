import tkinter as tk

class LineNumbers(tk.Canvas):
    def __init__(self, parent, editor, theme_manager, **kwargs):
        self.editor = editor
        self.theme_manager = theme_manager
        
        # Configure canvas attributes
        kwargs["width"] = 40
        kwargs["highlightthickness"] = 0
        
        super().__init__(parent, **kwargs)
        
        # Bind events
        self.editor.bind("<<TextModified>>", self.redraw, add="+")
        self.bind("<Configure>", self.redraw)
        
        # Trigger initial drawing
        self.redraw()

    def redraw(self, event=None):
        self.delete("all")
        
        # Get theme configuration
        theme = self.theme_manager.get_theme()
        bg_color = theme["line_numbers_bg"]
        fg_color = theme["line_numbers_fg"]
        curr_fg_color = theme.get("line_numbers_current_fg", theme["editor_fg"])
        
        self.configure(bg=bg_color)
        
        # Determine the number of lines to adjust canvas width
        try:
            num_lines = int(self.editor.index("end-1c").split(".")[0])
        except Exception:
            num_lines = 1
            
        # Dynamically measure width needed
        try:
            measured_width = self.editor.custom_font.measure(str(num_lines)) + 16
        except Exception:
            measured_width = 40
            
        width = max(40, measured_width)
        if self.winfo_width() != width and width > 40:
            self.configure(width=width)
            
        # Get the insert cursor line
        try:
            insert_line = int(self.editor.index("insert").split(".")[0])
        except Exception:
            insert_line = -1
            
        # Draw numbers for visible text lines
        try:
            top_idx = self.editor.index("@0,0")
            bottom_idx = self.editor.index(f"@0,{self.editor.winfo_height()}")
            
            top_line = int(top_idx.split(".")[0])
            bottom_line = int(bottom_idx.split(".")[0])
        except Exception:
            return
            
        for line_num in range(top_line, bottom_line + 1):
            line_idx = f"{line_num}.0"
            dline = self.editor.dlineinfo(line_idx)
            
            # dline is None if the line's start is not currently visible
            if dline is not None:
                y = dline[1]
                # Highlight current line number color
                color = curr_fg_color if line_num == insert_line else fg_color
                
                # Draw the number text aligned to the right side of the canvas
                self.create_text(
                    self.winfo_width() - 8, y,
                    anchor="ne",
                    text=str(line_num),
                    fill=color,
                    font=self.editor.custom_font
                )
