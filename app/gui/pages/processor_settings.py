import tkinter as tk
from tkinter import ttk
from gui.form import OptionsForm

class ProcessorSettingsPage(tk.Frame):

    def __init__(self, master = None, controller = None):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text = "Processor performance settings", font = ("Segoe UI", 14, "bold")).pack(pady = 5)
        OptionsForm(master = self)
    
    def apply_settings(self):
        pass