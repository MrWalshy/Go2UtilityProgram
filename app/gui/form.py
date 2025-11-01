import tkinter as tk
from tkinter import messagebox
from gui.widgets import NumericEntry, RadioGroup, Slider, SliderWithEntry
from logic.validators import validate_range
from logic.power_plan import get_active_power_scheme, set_p_core_limit, set_e_core_limit, set_cpu_boost_mode, set_energy_performance_preference
import subprocess

class OptionsForm(tk.Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack(padx = 10, pady = 10)
        self.create_widgets()

    def create_widgets(self):
        # p and e core limit fields
        # tk.Label(self, text = "CPU P Core limit (MHz):").grid(row = 0, column = 0, sticky = "w")
        # self.p_core_limit_entry = NumericEntry(self)
        # self.p_core_limit_entry.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.p_core_limit_slider = SliderWithEntry(
            self, label = "P-Core Frequency Limit",
            from_ = 0, to = 5000,
            unit = "MHz", help_text = "Adjust the maximum P-core clock limit, 0 = no limit."
        )
        self.p_core_limit_slider.grid(row = 0, columnspan = 2, padx = 10, pady = 10, sticky = "we")

        # tk.Label(self, text = "CPU E Core limit (MHz):").grid(row = 1, column = 0, sticky = "w")
        # self.e_core_limit_entry = NumericEntry(self)
        # self.e_core_limit_entry.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.e_core_limit_slider = SliderWithEntry(
            self, label = "P-Core Frequency Limit",
            from_ = 0, to = 3300,
            unit = "MHz", help_text = "Adjust the maximum E-core clock limit, 0 = no limit."
        )
        self.e_core_limit_slider.grid(row = 1, columnspan = 2, padx = 10, pady = 10, sticky = "we")

        # epp slider
        self.epp_slider = SliderWithEntry(
            self, label = "Energy Performance Preference",
            from_ = 0, to = 100, unit = "%",
            help_text = "0 prefers maximum CPU performance, 100 prefers highest energy saving"
        )
        self.epp_slider.grid(row = 2, columnspan = 2, padx = 10, pady = 10, sticky = "we")

        # cpu boost options
        self.cpu_boost_group = RadioGroup(
            "CPU Boost:", ["Enabled", "Disabled"], default = "Enabled", orient = "vertical", master = self
        )
        self.cpu_boost_group.grid(row = 3, columnspan = 2, sticky = "w", pady = 5)

        # submit button
        tk.Button(self, text = "Submit", command = self.submit).grid(
            row = 4, column = 0, columnspan = 2, pady = 10
        )

    def submit(self):
        # p_core_limit = 0 if self.p_core_limit_entry.get_value() == "" else int(self.p_core_limit_entry.get_value())
        # e_core_limit = 0 if self.e_core_limit_entry.get_value() == "" else int(self.e_core_limit_entry.get_value())
        p_core_limit = self.p_core_limit_slider.get_value()
        e_core_limit = self.e_core_limit_slider.get_value()
        epp_value = self.epp_slider.get_value()
        cpu_boost_mode = self.cpu_boost_group.get_value()
        error_message = ""
        error = False
        
        if not validate_range(p_core_limit, 0, 5000):
            error_message += "P core must be in range 0 - 5000\n"
            error = True
        if not validate_range(e_core_limit, 0, 3300):
            error_message += "E core must be in range 0 - 3300\n"
            error = True

        if error:
            messagebox.showerror("Error", error_message)
            return
        else:
            self.apply_settings(p_core_limit, e_core_limit, cpu_boost_mode, epp_value)

    def apply_settings(self, p_core_limit, e_core_limit, boost_mode, epp):
        try:
            active_plan = get_active_power_scheme()
            set_p_core_limit(active_plan, p_core_limit)
            set_e_core_limit(active_plan, e_core_limit)
            set_cpu_boost_mode(active_plan, boost_mode)
            set_energy_performance_preference(active_plan, epp)
            messagebox.showinfo("Result", f"Set P core limit to {p_core_limit}MHz,\nE core limit to {e_core_limit}Mhz,\nCPU Boost mode to {boost_mode}") 
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed:\n{e}")
