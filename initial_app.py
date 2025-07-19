import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Menu
import os
from datetime import datetime
import json
import re

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Note - untitled")
        self.root.geometry("400x300+1200+500")
        self.root.iconbitmap(self.get_default_icon())  # 使用默认图标
        
        # 初始化状态
        self.current_file = None
        self.is_topmost = tk.BooleanVar(value=True)  # 默认置顶
        self.root.attributes('-topmost', True)  # 初始设置为置顶
        
        # 创建UI
        self.create_menu()
        self.create_text_area()
        self.create_status_bar()
        
        # 绑定事件
        self.text.bind("<<Modified>>", self.on_text_modified)
        self.text.bind("<KeyRelease>", self.update_status_bar)
        
        self.text.focus_set()  # 设置焦点到文本区域
        self.root.after(100, lambda: self.text.focus_force())  # 确保焦点锁定

    def get_default_icon(self):
        """获取默认Fast Note图标"""
        try:
            # 尝试使用Windows自带的Fast Note图标
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\notepad.exe")
            notepad_path = winreg.QueryValue(key, None)
            return notepad_path
        except:
            # 如果无法获取，则使用默认图标
            return None
    
    def create_menu(self):
        """创建菜单栏"""
        menu_bar = Menu(self.root)
        
        # 文件菜单
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New File", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open File...", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save File", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save as...", command=self.save_as)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # 编辑菜单
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="undo", accelerator="Ctrl+Z", command=lambda: self.text.edit_undo())
        edit_menu.add_command(label="redo", accelerator="Ctrl+Y", command=lambda: self.text.edit_redo())
        edit_menu.add_separator()
        edit_menu.add_command(label="cut", accelerator="Ctrl+X", command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="copy", accelerator="Ctrl+C", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="paste", accelerator="Ctrl+V", command=lambda: self.text.event_generate("<<Paste>>"))
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # save to subject,   列出vault中所有的文件夹作为subject
        # 最后一栏选择适当的文件夹作为vault

        # Quik Save
        # quik save to scratch and close (q)， 快速将其保存至当前小时或者上一个小时的文本中，并添加时间。
        # quik save to journal and close (j)， 跳出一个栏，每个subject对应一个快捷键。

        # mode 
        # 高级功能，选择文本文件或是数据库的交互，创建出两列，若干个格子，左边用于粘贴图像，右边用于写对应的文本
        # 升级：可以选择若干栏，类似spread sheet，可以选择一列是用来作粘贴图片还是书写文字
        # 操作方面，需要shift+方向键实现在不同格子间的跨越，同时创作模式和观看模式也要做区分。

        # 添加置顶按钮
        top_menu = Menu(menu_bar, tearoff=0)
        top_menu.add_checkbutton(
            label="topmost", 
            variable=self.is_topmost, 
            command=self.toggle_topmost,
            selectcolor="sky blue"  # 选中时的背景色
        )
        menu_bar.add_cascade(label="topmost", menu=top_menu)
        
        self.root.config(menu=menu_bar)
        
        # 添加快捷键
        self.root.bind_all("<Control-n>", lambda e: self.new_file())
        self.root.bind_all("<Control-o>", lambda e: self.open_file())
        self.root.bind_all("<Control-s>", lambda e: self.save_file())
   
    def create_text_area(self):
        """创建文本编辑区"""
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            undo=True,
            font=("宋体", 15)
        )
        self.text.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = tk.Label(
            self.root, 
            text="Ln: 1, Col: 1  |  0 characters", 
            bd=1, 
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def toggle_topmost(self):
        """切换置顶状态"""
        topmost = self.is_topmost.get()
        self.root.attributes('-topmost', topmost)
        
        # 更新菜单项选中状态
        menu = self.root.nametowidget(".!menu.5")  # 获取置顶菜单
        menu.entryconfig(0, label="取消置顶" if topmost else "置顶")
    
    def update_status_bar(self, event=None):
        """更新状态栏信息"""
        cursor_pos = self.text.index(tk.INSERT)
        line, column = map(int, cursor_pos.split('.'))
        self.status_bar.config(text=f"Ln: {line}, Col: {column + 1}")
    
    def toggle_status_bar(self):
        """切换状态栏显示"""
        if self.status_bar_visible.get():
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            self.status_bar.pack_forget()
    
    def toggle_word_wrap(self):
        """切换自动换行"""
        self.text.config(wrap=tk.WORD if self.word_wrap.get() else tk.NONE)
    
    def set_font(self):
        """设置字体"""
        font = "Consolas"  # 简化实现，实际应用中应打开字体选择对话框
        self.text.config(font=(font, 10))
    
    def new_file(self):
        """新建文件"""
        if self.text.edit_modified():
            if not self.prompt_save():
                return
        
        self.text.delete(1.0, tk.END)
        self.text.edit_modified(False)
        self.current_file = None
        self.root.title("Fast Note - untitled")
    
    def open_file(self):
        """打开文件"""
        if self.text.edit_modified():
            if not self.prompt_save():
                return
        
        file_path = filedialog.askopenfilename(
            filetypes=[("文本文档", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text.delete(1.0, tk.END)
                    self.text.insert(tk.END, file.read())
                
                self.current_file = file_path
                self.root.title(f"Fast Note - {os.path.basename(file_path)}")
                self.text.edit_modified(False)
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件: {str(e)}")
    
    def save_file(self):
        """保存文件"""
        if self.current_file:
            try:
                content = self.text.get(1.0, tk.END)
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(content)
                
                self.text.edit_modified(False)
                return True
            except Exception as e:
                messagebox.showerror("错误", f"无法保存文件: {str(e)}")
                return False
        else:
            return self.save_as()
    
    def save_as(self):
        """Save As file"""
        # 生成以今日日期和时间命名的默认文件名（格式：YYYYMMDD_HH.txt）
        default_filename = datetime.now().strftime("%Y-%m-%d_%H") + ".txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")],
            initialfile=default_filename  # 设置默认文件名
        )
        
        if file_path:
            try:
                content = self.text.get(1.0, tk.END)
                
                # 在文件内容第一行添加当前日期和星期
                today = datetime.now()
                date_line = today.strftime("%Y.%m.%d") + " " + today.strftime("%A") + "\n" + "\n"
                
                # 如果第一行已经有内容，就在前面添加日期行
                # 如果第一行是空行，则替换为日期行
                first_line = self.text.get(1.0, "1.end")
                if first_line.strip() != "":
                    content = date_line + content
                else:
                    content = date_line + self.text.get(1.1, tk.END)
                
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                
                self.current_file = file_path
                self.root.title(f"Fast Note - {os.path.basename(file_path)}")
                self.text.edit_modified(False)
                
                # 在编辑器中显示添加的日期行
                self.text.insert(1.0, date_line)
                self.text.edit_modified(False)  # 重置修改标志
                
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save file: {str(e)}")
                return False
        return False
    
    def prompt_save(self):
        """保存提示对话框"""
        response = messagebox.askyesnocancel(
            "Fast Note",
            "是否保存对文件的更改？"
        )
        
        if response is None:  # 取消
            return False
        elif response:  # 是
            return self.save_file()
        else:  # 否
            return True
    
    def on_text_modified(self, event=None):
        """文本修改时的处理"""
        if self.text.edit_modified():
            if self.current_file:
                title = self.root.title()
                if not title.startswith("*"):
                    self.root.title("*" + title)
            else:
                self.root.title("*Fast Note - untitled")
        self.text.edit_modified(False)  # 重置modified标志

if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()