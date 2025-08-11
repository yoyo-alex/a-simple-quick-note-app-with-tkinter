import tkinter as tk

class StatusBar:
    def __init__(self, parent, app):
        self.app = app
        self.label = tk.Label(
            parent,
            text=f"Ln: 0 , Col: 0  |  Characters: 0 , Words: 0",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update(self, line, column, characters, words):
        new_text = f"Ln: {line} , Col: {column}  |  Characters: {characters} , Words: {words}"
        self.label.config(
            text=new_text
        )