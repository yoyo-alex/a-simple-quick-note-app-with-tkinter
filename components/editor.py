import tkinter as tk
from tkinter import scrolledtext
from tkinter import font

class Editor:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        text_font = font.Font(family="Consolas", size=11)

        self.text = scrolledtext.ScrolledText(
            self.frame,
            wrap=tk.WORD,
            undo=True,
            font=text_font
        )

        # 设置 Tab 宽度（仅影响光标跳动和对齐效果）
        tab_width = text_font.measure(" " * 4)
        self.text.config(tabs=(tab_width,))
        # 绑定 Tab 键，插入 4 个空格
        self.text.bind("<Tab>", self.insert_spaces)
        self.text.pack(fill=tk.BOTH, expand=True)
        
    def insert_spaces(self, event):
        """按 Tab 插入四个空格"""
        self.text.insert(tk.INSERT, " " * 4)
        return "break"  # 阻止默认 \t 插入

    def focus(self):
        self.text.focus_set()
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
    
    def get_content(self):
        return self.text.get(1.0, tk.END)
    
    def set_content(self, content):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, content)
    
    def is_modified(self):
        return self.text.edit_modified()
    
    def reset_modified(self):
        self.text.edit_modified(False)
    
    def insert_date_header(self):
        from datetime import datetime
        today = datetime.now()
        date_line = today.strftime("%Y.%m.%d") + " " + today.strftime("%A") + "\n\n"
        self.text.insert("1.0", date_line)
