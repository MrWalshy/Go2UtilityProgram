import tkinter as tk
from tkinter import ttk
from gui.form import OptionsForm
from gui.pages.page import Page

class ProcessorSettingsPage(Page):

    def __init__(self, master = None):
        super().__init__(master)

        tk.Label(self, text = "Processor performance settings", font = ("Segoe UI", 14, "bold")).pack(pady = 5)
        OptionsForm(master = self)
