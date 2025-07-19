import tkinter as tk

class StatusBar:
    def __init__(self, parent, app):
        self.app = app
        self.label = tk.Label(
            parent,
            text="Ln: 1, Col: 1  |  0 characters",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update(self, line, column, char_count):
        """更新状态栏信息"""
        vault_info = ""
        if self.app.file_manager.vault_path:
            vault_name = self.app.file_manager.vault_name()
            vault_info = f" | Vault: {vault_name}"
        
        self.label.config(
            text=f"Ln: {line}, Col: {column}  |  {char_count} characters{vault_info}"
        )