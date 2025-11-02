import tkinter as tk
from tkinter import ttk

class PowerSettingsPage(tk.Frame):

    def __init__(self, master = None, controller = None):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text = "Power settings", font = ("Segoe UI", 14, "bold")).pack(pady = 5)
        text = tk.Text(self)
        text.insert("1.0", "To be decided...\n")
        text.insert("2.0", "Exploring options for Auto TSP and Auto TDP features\n")
        text.insert("3.0", "- Auto TSP: Auto adjusts TDP to maintain a target total system power.\n")
        text.insert("4.0", "- Auto TDP: Auto adjusts TDP to maintain a specified FPS in game.")
        text.pack(pady = 5)
    
    def apply_settings(self):
        pass