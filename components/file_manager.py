import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

class FileManager:
    def __init__(self, app):
        self.app = app
        self.current_file = None
        self.vault_path = None
        self.scratch_path = None
        self._init_vault()
    
    def _init_vault(self):
        """初始化工作区"""
        # 尝试加载配置
        if self.app.config.get("vault_path"):
            self.vault_path = self.app.config.get("vault_path")
            self.scratch_path = os.path.join(self.vault_path, "scratch")
            os.makedirs(self.scratch_path, exist_ok=True)
        else:
            # 如果没有配置，提示用户选择
            self.choose_vault()
    
    def vault_name(self):
        """获取vault名称"""
        if self.vault_path:
            return os.path.basename(self.vault_path)
        return ""
    
    def choose_vault(self):
        """选择工作文件夹(vault)"""
        vault_path = filedialog.askdirectory(
            title="Select Your Vault Folder",
            mustexist=True
        )
        if vault_path:
            self.vault_path = vault_path
            # 在vault中创建scratch文件夹
            self.scratch_path = os.path.join(self.vault_path, "scratch")
            os.makedirs(self.scratch_path, exist_ok=True)
            # 保存配置
            self.app.config.set("vault_path", vault_path)
            self.app.config.save_config()
            # 更新状态栏
            self.app.status_bar.update(1, 1, 0)
            # 显示成功消息
            messagebox.showinfo(
                "Vault Selected", 
                f"Vault set to:\n{self.vault_path}\n"
                f"Scratch folder: {self.scratch_path}"
            )
    
    def new_file(self):
        """创建新文件"""
        if self.app.editor.is_modified():
            if not self.prompt_save():
                return
        
        # 清空编辑器
        self.app.editor.set_content("")
        
        # 添加日期标题
        self.app.editor.insert_date_header()
        
        # 重置状态
        self.app.editor.reset_modified()
        self.current_file = None
        self.app.root.title("Quick Note - untitled")
        self.app.status_bar.update(1, 1, 0)
        
        # 设置焦点
        self.app.editor.focus()
        self.app.editor.text.mark_set(tk.INSERT, "3.0")  # 光标移到日期行后面
        self.app.editor.text.see(tk.INSERT)
    
    def open_file(self):
        """打开文件"""
        if self.app.editor.is_modified():
            if not self.prompt_save():
                return
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.app.editor.set_content(file.read())
                
                self.current_file = file_path
                self.app.root.title(f"Quick Note - {os.path.basename(file_path)}")
                self.app.editor.reset_modified()
                self.app.update_status()
                
                # 检查并添加日期行
                first_line = self.app.editor.text.get("1.0", "1.end")
                if not re.match(r"\d{4}\.\d{2}\.\d{2} [A-Za-z]+day", first_line):
                    self.app.editor.insert_date_header()
                
                # 设置焦点
                self.app.editor.focus()
                self.app.editor.text.mark_set(tk.INSERT, tk.END)
                self.app.editor.text.see(tk.INSERT)
                
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open file: {str(e)}")
    
    def save_file(self):
        """保存文件"""
        if self.current_file:
            try:
                content = self.app.editor.get_content()
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(content)
                
                self.app.editor.reset_modified()
                self.app.root.title(f"Quick Note - {os.path.basename(self.current_file)}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save file: {str(e)}")
                return False
        else:
            return self.save_as()
    
    def save_as(self):
        """另存为文件"""
        # 确定初始目录
        initial_dir = self.scratch_path if self.scratch_path else "."
        
        # 创建默认文件名（当前日期+时间）
        default_filename = datetime.now().strftime("%Y-%m-%d_%H") + ".txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")],
            initialdir=initial_dir,
            initialfile=default_filename
        )
        
        if file_path:
            try:
                # 确保有日期标题
                first_line = self.app.editor.text.get("1.0", "1.end")
                if not re.match(r"\d{4}\.\d{2}\.\d{2} [A-Za-z]+day", first_line):
                    self.app.editor.insert_date_header()
                
                # 保存内容
                content = self.app.editor.get_content()
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                
                self.current_file = file_path
                self.app.root.title(f"Quick Note - {os.path.basename(file_path)}")
                self.app.editor.reset_modified()
                
                messagebox.showinfo("Save Success", f"File saved to:\n{file_path}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save file: {str(e)}")
                return False
        return False
    
    def prompt_save(self):
        """保存提示对话框"""
        response = messagebox.askyesnocancel(
            "Quick Note",
            "Do you want to save changes to this file?"
        )
        
        if response is None:  # 取消
            return False
        elif response:  # 是
            return self.save_file()
        else:  # 否
            return True