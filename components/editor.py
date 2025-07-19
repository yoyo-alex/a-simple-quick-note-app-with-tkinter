import tkinter as tk
from tkinter import scrolledtext

class Editor:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.text = scrolledtext.ScrolledText(
            self.frame,
            wrap=tk.WORD,
            undo=True,
            font=("Segoe UI", 12)
        )
        self.text.pack(fill=tk.BOTH, expand=True)
    
    def focus(self):
        """设置焦点到编辑器"""
        self.text.focus_set()
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
    
    def get_content(self):
        """获取编辑器内容"""
        return self.text.get(1.0, tk.END)
    
    def set_content(self, content):
        """设置编辑器内容"""
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, content)
    
    def is_modified(self):
        """检查内容是否修改"""
        return self.text.edit_modified()
    
    def reset_modified(self):
        """重置修改状态"""
        self.text.edit_modified(False)
    
    def insert_date_header(self):
        """插入日期标题"""
        from datetime import datetime
        today = datetime.now()
        date_line = today.strftime("%Y.%m.%d") + " " + today.strftime("%A") + "\n\n"
        self.text.insert("1.0", date_line)