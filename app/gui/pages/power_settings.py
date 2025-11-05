import tkinter as tk
from tkinter import ttk
from gui.pages.page import Page

class PowerSettingsPage(Page):

    def __init__(self, master = None):
        super().__init__(master)

        tk.Label(self, text = "Power settings", font = ("Segoe UI", 14, "bold")).pack(pady = 5)
        text = tk.Text(self)
        text.insert("1.0", "To be decided...\n")
        text.insert("2.0", "Exploring options for Auto TSP and Auto TDP features\n")
        text.insert("3.0", "- Auto TSP: Auto adjusts TDP to maintain a target total system power.\n")
        text.insert("4.0", "- Auto TDP: Auto adjusts TDP to maintain a specified FPS in game.")
        text.pack(pady = 5)
    