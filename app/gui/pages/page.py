import tkinter as tk

class Page(tk.Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self._is_visible = False

    def on_show(self):
        self._is_visible = True

    def on_hide(self):
        self._is_visible = False