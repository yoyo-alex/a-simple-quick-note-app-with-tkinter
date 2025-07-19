from tkinter import Menu

class MenuManager:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.menu_bar = Menu(root)
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()  # 单独创建视图菜单
        root.config(menu=self.menu_bar)
    
    def _create_file_menu(self):
        """创建菜单栏"""
        # 文件菜单
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New File", accelerator="Ctrl+N", command=self.app.new_file)
        file_menu.add_command(label="Open File...", accelerator="Ctrl+O", command=self.app.open_file)
        file_menu.add_command(label="Save File", accelerator="Ctrl+S", command=self.app.save_file)
        file_menu.add_command(label="Save as...", command=self.app.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Choose Vault", command=self.app.choose_vault)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_edit_menu(self):       
        # 编辑菜单
        edit_menu = Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: self.app.editor.text.edit_undo())
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: self.app.editor.text.edit_redo())
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.app.editor.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.app.editor.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.app.editor.text.event_generate("<<Paste>>"))
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
    def _create_view_menu(self):   
        """单独创建视图菜单（包含置顶选项）"""
        # 确保应用已经完全初始化
        if not hasattr(self.app, 'is_topmost'):
            # 等待100ms后再次尝试创建
            self.root.after(100, self._create_view_menu)
            return
            
        view_menu = Menu(self.menu_bar, tearoff=0)
        self.top_menu = Menu(view_menu, tearoff=0)
        self.top_menu.add_checkbutton(
            label="Topmost" if self.app.is_topmost.get() else "Untop",
            variable=self.app.is_topmost,
            command=self.app.toggle_topmost,
            selectcolor="sky blue"
        )
        view_menu.add_cascade(label="View", menu=self.top_menu)
        self.menu_bar.add_cascade(label="View", menu=view_menu) 
        
        # 添加快捷键
        self.root.bind_all("<Control-n>", lambda e: self.app.new_file())
        self.root.bind_all("<Control-o>", lambda e: self.app.open_file())
        self.root.bind_all("<Control-s>", lambda e: self.app.save_file())
    
    def update_topmost_label(self, topmost):
        """更新置顶菜单标签"""
        if hasattr(self, 'top_menu'):
            self.top_menu.entryconfig(0, label="Untop" if topmost else "Topmost")