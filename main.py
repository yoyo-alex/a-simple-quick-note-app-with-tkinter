import tkinter as tk
from app import NotepadApp
import ctypes

if __name__ == "__main__":
    root = tk.Tk()
    try:
        # Windows系统DPI优化方案
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # 获取系统缩放比例
        scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        root.tk.call('tk', 'scaling', scaleFactor * 1.5)  # 额外增加50%放大
    except:
        # 其他系统使用默认放大
        root.tk.call('tk', 'scaling', 2.0)
    app = NotepadApp(root)
    root.mainloop()