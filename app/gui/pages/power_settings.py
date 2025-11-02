import tkinter as tk
from tkinter import ttk

class PowerSettingsPage(tk.Frame):

    def __init__(self, master = None, controller = None):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text = "Power settings", font = ("Segoe UI", 14, "bold")).pack(pady = 5)
    
    def apply_settings(self):
        pass