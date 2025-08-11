import tkinter as tk
from components.editor import Editor
from components.status_bar import StatusBar
from components.menu_manager import MenuManager
from components.file_manager import FileManager
from config import ConfigManager
from tkinter import filedialog, Toplevel, Text, Scrollbar
import os
from ctypes import windll
import re

# app.py
class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Note - untitled")
        self.root.geometry("650x433+1600+800")
        self.root.iconbitmap("quicknote.ico")
        # ===== 首先初始化所有状态属性 =====
        self.is_topmost = tk.BooleanVar(value=True)  # 确保在创建菜单前初始化
        self.root.attributes('-topmost', True)
        
        # 初始化配置管理
        self.config = ConfigManager()
        self.config.load_config()
        
        # ===== 然后初始化组件 =====
        self.editor = Editor(self.root, self)
        self.file_manager = FileManager(self)
        self.status_bar = StatusBar(self.root, self)
        self.menu_manager = MenuManager(self.root, self)
        
        # 绑定事件
        self._bind_events()
        
        # 设置焦点到编辑器
        self.editor.focus()
    
    def _bind_events(self):
        """绑定应用级事件"""
        self.editor.text.bind("<<Modified>>", self.on_text_modified)
        self.editor.text.bind("<KeyRelease>", self.update_status)
    
    def update_status(self, event=None):
        """更新状态栏"""
        cursor_pos = self.editor.text.index(tk.INSERT)
        line, column = map(int, cursor_pos.split('.'))
        content = self.editor.text.get("1.0", "end-1c")
        characters = len(content)
        pattern = r'''
            [a-zA-Z]+(?:['-][a-zA-Z]+)*|  # 英文单词（含连字符和撇号）
            [\u4e00-\u9fff]|              # 单个中文字符
            \d+|                          # 数字序列
            [a-zA-Z0-9]+                  # 字母数字混合（如iPhone15）
        '''
        words = len(re.findall(pattern, content, re.VERBOSE))
        self.status_bar.update(line, column + 1, characters, words)
    
    def on_text_modified(self, event=None):
        """处理文本修改事件"""
        if self.editor.text.edit_modified():
            title = self.root.title()
            if not title.startswith("*"):
                self.root.title("*" + title)
        self.editor.text.edit_modified(False)
    
    def toggle_topmost(self):
        """切换窗口置顶状态"""
        topmost = self.is_topmost.get()
        self.root.attributes('-topmost', topmost)
        self.menu_manager.update_topmost_label(topmost)
    
    # 文件操作代理方法
    def new_file(self):
        self.file_manager.new_file()
    def open_file(self):
        self.file_manager.open_file()
    def save_file(self):
        self.file_manager.save_file()
    def save_as(self):
        self.file_manager.save_as()
    def prompt_save(self):
        return self.file_manager.prompt_save()
    def choose_vault(self):
        self.file_manager.choose_vault()

    # overview功能的实现
    def batch_preview(self):
        """批量预览功能"""
        folder_path = filedialog.askdirectory(title="Select Folder with TXT Files")
        if not folder_path:
            return
            
        # 创建预览窗口
        preview_win = Toplevel(self.root)
        preview_win.title(f"overview - {os.path.basename(folder_path)}")
        preview_win.geometry("900x700")
        
        try:
            windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor DPI aware
            scale_factor = windll.shcore.GetScaleFactorForDevice(0) / 100
            preview_win.tk.call('tk', 'scaling', scale_factor * 1.5)  # 额外放大20%
        except Exception as e:
            # 非Windows系统或API不可用时的回退方案
            preview_win.tk.call('tk', 'scaling', 2.0)  # 默认放大200%
        
        # 文本显示区域
        text_frame = tk.Frame(preview_win)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_area = Text(text_frame, wrap="word",font=("Consolas", 10))
        scrollbar = Scrollbar(text_frame, command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        text_area.pack(side="left", fill="both", expand=True)
        
        # 处理文件内容
        txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        txt_files.sort()  # 按文件名排序
        
        content = ""
        for txt_file in txt_files:
            file_path = os.path.join(folder_path, txt_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # 添加文件名作为标题
                    content += f"\n\n{'='*50}\n{txt_file}\n{'='*50}\n\n"
                    content += f.read()
            except Exception as e:
                content += f"\n\nError reading {txt_file}: {str(e)}\n"
                
        text_area.insert("1.0", content)