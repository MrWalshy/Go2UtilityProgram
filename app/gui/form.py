import tkinter as tk
from tkinter import ttk, messagebox
from gui.widgets import RadioGroup, SliderWithEntry
from logic.validators import validate_range
from logic.power_plan import get_active_power_scheme, set_p_core_limit, set_e_core_limit, set_cpu_boost_mode, set_energy_performance_preference, get_e_core_limit, get_p_core_limit, get_cpu_boost_mode, get_energy_performance_preference
import subprocess

class OptionsForm(tk.Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack(padx = 10, pady = 10)
        self.create_widgets()

    def load_values(self):
        plan = get_active_power_scheme()
        p_core_value =  get_p_core_limit(plan)
        e_core_value = get_e_core_limit(plan)
        epp_value = get_energy_performance_preference(plan)
        cpu_boost_value = get_cpu_boost_mode(plan)

        if p_core_value is not None:
            self.p_core_limit_slider.set_value(p_core_value)
        if e_core_value is not None:
            self.e_core_limit_slider.set_value(e_core_value)
        if epp_value is not None:
            self.epp_slider.set_value(epp_value)
        if cpu_boost_value is not None:
            self.cpu_boost_group.set_value("Disabled" if cpu_boost_value == 0 else "Enabled")

    def create_widgets(self):
        # options checkbox vars
        self.apply_p_core = tk.BooleanVar(value = False)
        self.apply_e_core = tk.BooleanVar(value = False)
        self.apply_epp = tk.BooleanVar(value = False)
        self.apply_cpu_boost = tk.BooleanVar(value = False)

        # p and e core limit fields
        p_frame = ttk.Frame(self)
        p_frame.grid(row = 0, columnspan = 2, padx = 10, pady = 10, sticky = "we")
        ttk.Checkbutton(p_frame, text = "Apply", variable = self.apply_p_core).pack(side = "left", padx = 5)
        self.p_core_limit_slider = SliderWithEntry(
            p_frame, label = "P-Core Frequency Limit",
            from_ = 0, to = 5000,
            unit = "MHz", help_text = "Adjust the maximum P-core clock limit, 0 = no limit.\nNote: Values below ~1225, except 0, cause the P-core clocks to get stuck at ~600MHz."
        )
        self.p_core_limit_slider.pack(fill = "x", expand = True, padx = 5)

        e_frame = ttk.Frame(self)
        e_frame.grid(row = 1, columnspan = 2, padx = 10, pady = 10, sticky = "we")
        ttk.Checkbutton(e_frame, text = "Apply", variable = self.apply_e_core).pack(side = "left", padx = 5)
        self.e_core_limit_slider = SliderWithEntry(
            e_frame, label = "E-Core Frequency Limit",
            from_ = 0, to = 3300,
            unit = "MHz", help_text = "Adjust the maximum E-core clock limit, 0 = no limit.\nNote: Values below ~1225, except 0, cause the E-core clocks to get stuck at ~600MHz."
        )
        self.e_core_limit_slider.pack(fill = "x", expand = True, padx = 5)

        # epp slider
        epp_frame = ttk.Frame(self)
        epp_frame.grid(row = 2, columnspan = 2, padx = 10, pady = 10, sticky = "we")
        ttk.Checkbutton(epp_frame, text = "Apply", variable = self.apply_epp).pack(side = "left", padx = 5)
        self.epp_slider = SliderWithEntry(
            epp_frame, label = "Energy Performance Preference",
            from_ = 0, to = 100, unit = "%",
            help_text = "0 prefers maximum CPU performance, 100 prefers highest energy saving"
        )
        self.epp_slider.pack(fill = "x", expand = True, padx = 5)

        # cpu boost options
        boost_frame = ttk.Frame(self)
        boost_frame.grid(row = 3, columnspan = 2, sticky = "w", pady = 5)
        ttk.Checkbutton(boost_frame, text = "Apply", variable = self.apply_cpu_boost).pack(side = "left", padx = 5)
        self.cpu_boost_group = RadioGroup(
            "CPU Boost:", ["Enabled", "Disabled"], default = "Enabled", orient = "vertical", master = boost_frame
        )
        self.cpu_boost_group.pack(fill = "x", expand = True, padx = 5)

        # submit button
        tk.Button(self, text = "Submit", command = self.submit).grid(
            row = 4, column = 0, columnspan = 2, pady = 10
        )
        self.load_values()

    def submit(self):
        self.focus_set() # force focus away from inputs to fire focus out events
        settings = []

        if self.apply_p_core.get():
            value = self.p_core_limit_slider.get_value()
            settings.append(("P-Core Limit (MHz)", set_p_core_limit, value))
        
        if self.apply_e_core.get():
            value = self.e_core_limit_slider.get_value()
            settings.append(("E-Core Limit (MHz)", set_e_core_limit, value))

        if self.apply_epp.get():
            value = self.epp_slider.get_value()
            settings.append(("EPP Limit (%)", set_energy_performance_preference, value))
        
        if self.apply_cpu_boost.get():
            value = self.cpu_boost_group.get_value()
            settings.append(("CPU Boost Mode", set_cpu_boost_mode, value))
        
        try:
            summary = ""
            active_plan = get_active_power_scheme()
            for label, fn, value in settings:
                fn(active_plan, value)
                summary += f"{label}: {value}\n"
            messagebox.showinfo("Result", f"Applied:\n{summary}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed:\n{e}")

    def apply_settings(self, p_core_limit, e_core_limit, boost_mode, epp):
        try:
            active_plan = get_active_power_scheme()
            set_p_core_limit(active_plan, p_core_limit)
            set_e_core_limit(active_plan, e_core_limit)
            set_cpu_boost_mode(active_plan, boost_mode)
            set_energy_performance_preference(active_plan, percentage = epp)
            messagebox.showinfo("Result", f"Set P core limit to {p_core_limit}MHz,\nE core limit to {e_core_limit}Mhz,\nCPU Boost mode to {boost_mode},\nEPP to {epp}%") 
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed:\n{e}")
