import tkinter as tk
from tkinter import ttk
from gui.pages.page import Page

from logic.commands.ryzenadj_commands import *
from logic.commands.system_info_commands import *

class SystemOverviewPage(Page):

    def __init__(self, master = None, refresh_interval = 1000):
        """
        
        Preconditions:
        - 'refresh' is in milliseconds
        """
        super().__init__(master)
        self.refresh_interval = refresh_interval
        self._refresh_job = None
        self._create_widgets()
        
    
    def _create_widgets(self):
        # scrollable frame
        canvas = tk.Canvas(self, borderwidth = 0, highlightthickness = 0)
        scrollbar = ttk.Scrollbar(self, orient = "vertical", command = canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion = canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window = self.scrollable_frame, anchor = "nw")
        canvas.configure(yscrollcommand = scrollbar.set)
        canvas.pack(side = "left", fill = "both", expand = True)
        scrollbar.pack(side = "right", fill = "y")

        # content
        tk.Label(self.scrollable_frame, text = "System overview", font = ("Segoe UI", 14, "bold")).pack(pady = 5)

        # value labels
        self.system_info_labels = {
            "System": ttk.Label(self.scrollable_frame, text="System: --", style="Value.TLabel"),
            "Processor": ttk.Label(self.scrollable_frame, text="Processor: --", style="Value.TLabel"),
            "Version": ttk.Label(self.scrollable_frame, text="Version: --", style="Value.TLabel"),
            "Machine": ttk.Label(self.scrollable_frame, text="Machine: --", style="Value.TLabel"),

            "Cores": ttk.Label(self.scrollable_frame, text="Cores: --", style="Value.TLabel"),
            "Logical_cores": ttk.Label(self.scrollable_frame, text="Logical cores: --", style="Value.TLabel"),
            "Max_freq": ttk.Label(self.scrollable_frame, text="Max frequency: --", style="Value.TLabel"),
            "Min_freq": ttk.Label(self.scrollable_frame, text="Min frequency: --", style="Value.TLabel"),
            "Current_freq": ttk.Label(self.scrollable_frame, text="Current frequency: --", style="Value.TLabel"),
        }

        for label in self.system_info_labels.values():
            label.pack(anchor = "w", padx = 10, pady = 2)
        
        # styling - need to look more into ttk styling
        style = ttk.Style(self)
        style.configure("Value.TLabel", font = ("Consolas", 10))

    def on_show(self):
        """Call when navigating to the page to start refreshing data."""
        super().on_show()
        self._refresh()
    
    def on_hide(self):
        """Call when navigating away from this page to stop refreshing data"""
        super().on_hide()
        if self._refresh_job:
            self.after_cancel(self._refresh_job)
            self._refresh_job = None
    
    def _refresh(self):
        if not self._is_visible:
            return
        
        try:
            sys_info = GetSystemInfo()
            cpu_info = GetCpuInfo()

            for cmd in [sys_info, cpu_info]:
                cmd.execute()

            self._update_static_sys_info_labels(sys_info, cpu_info)
            self._update_cpu_info_labels(cpu_info)
        except Exception as e:
            print(f"[System Overview] Refresh failed: {e}")
        
        self._refresh_job = self.after(self.refresh_interval, self._refresh)
    
    def _update_static_sys_info_labels(self, sys_info: dict, cpu_info: dict) -> None:
        if self._refresh_job:
            return
        print("[System Overview] Updating static labels")
        self.system_info_labels["System"].config(text = f"System: {sys_info.value['system']}")
        self.system_info_labels["Processor"].config(text = f"Processor: {sys_info.value['processor']}")
        self.system_info_labels["Version"].config(text = f"Version: {sys_info.value['version']}")
        self.system_info_labels["Machine"].config(text = f"Machine: {sys_info.value['machine']}")
        self.system_info_labels["Cores"].config(text = f"Cores: {cpu_info.value["cores"]}")
        self.system_info_labels["Logical_cores"].config(text = f"Logical cores: {cpu_info.value["logical_cores"]}")

    def _update_cpu_info_labels(self, cpu_info: dict) -> None:
        print("[System Overview] Updating CPU info labels")
        self.system_info_labels["Max_freq"].config(text = f"Max frequency: {cpu_info.value['max_frequency']}")
        self.system_info_labels["Min_freq"].config(text = f"Min frequency: {cpu_info.value['min_frequency']}")
        self.system_info_labels["Current_freq"].config(text = f"Current frequency: {cpu_info.value['current_frequency']}")
        