import tkinter as tk
from components.editor import Editor
from components.status_bar import StatusBar
from components.menu_manager import MenuManager
from components.file_manager import FileManager
from config import ConfigManager

# app.py
class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Note - untitled")
        self.root.geometry("400x300+1200+500")
        
        # ===== 首先初始化所有状态属性 =====
        self.is_topmost = tk.BooleanVar(value=True)  # 确保在创建菜单前初始化
        self.root.attributes('-topmost', True)
        
        # 初始化配置管理
        self.config = ConfigManager()
        self.config.load_config()
        
        # ===== 然后初始化组件 =====
        self.editor = Editor(self.root, self)
        self.status_bar = StatusBar(self.root, self)
        self.file_manager = FileManager(self)
        self.menu_manager = MenuManager(self.root, self)  # 菜单最后初始化
        
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
        content = self.editor.text.get(1.0, tk.END)
        char_count = len(content) - 1
        self.status_bar.update(line, column + 1, char_count)
    
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