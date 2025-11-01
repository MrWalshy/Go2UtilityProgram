import tkinter as tk
from tkinter import ttk
from logic.validators import validate_numeric
import os
import subprocess

def show_touch_keyboard(event = None):
    possible_paths = [
        r"C:\Program Files\Common Files\Microsoft Shared\ink\TabTip.exe",
        r"C:\Program Files (x86)\Common Files\Microsoft Shared\ink\TabTip.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            subprocess.Popen([path], shell=True)
            break

class NumericEntry(tk.Entry):

    def __init__(self, master = None, **kwargs):
        self.var = tk.StringVar() # for storing the entry input text
        # validate = 'key' says validate on each keystroke
        super().__init__(master, textvariable = self.var, validate = "key", **kwargs)
        # wrap the validate method so Tkinter can call it it, 'validatecommand'
        # expects a callable with substitute values (%P) is the new value
        self['validatecommand'] = (self.register(self._on_validate), '%P')
        self.bind("<FocusIn>", show_touch_keyboard)

    def _on_validate(self, new_value):
        return validate_numeric(new_value)

    def get_value(self):
        return self.var.get()

class RadioGroup(ttk.Radiobutton):

    def __init__(self, label_text, options, default = None, orient = "horizontal", master = None, **kwargs):
        super().__init__(master, **kwargs)
        self.var = tk.StringVar()

        if default and default in options:
            self.var.set(default)
        elif options:
            self.var.set(options[0])

        # label
        self.label = tk.Label(self, text = label_text)
        self.label.pack(side = "top" if orient == "vertical" else "left", padx = 5, pady = 2)

        # buttons
        for opt in options:
            radio_button = tk.Radiobutton(self, text = opt, variable = self.var, value = opt)
            if orient == "vertical":
                radio_button.pack(anchor = "w")
            else:
                radio_button.pack(side = "left")

    def get_value(self):
        return self.var.get()

    def set_value(self, value):
        self.var.set(value)

class Slider(tk.Frame):

    def __init__(self, master = None, label = "", from_ = 0, to = 100, unit="", help_text = None, **kwargs):
        super().__init__(master)
        self.label_text = label
        self.unit = unit

        # slider label
        self.label = tk.Label(self, text = self.label_text)
        self.label.pack(anchor = "w")

        # widget scale
        self.scale = tk.Scale(self, from_ = from_, to = to, orient = "horizontal", **kwargs)
        self.scale.pack(fill = "x", expand = True)

        # display value label below slider
        self.value_label = tk.Label(self, text = f"{self.scale.get()} {self.unit}")
        self.value_label.pack(anchor = "w", pady = (2, 0))

        # update value label as slider moves
        self.scale.bind("<Motion>", self._update_value)
        self.scale.bind("<ButtonRelease-1>", self._update_value)

        # help text (if any)
        if help_text:
            self.help_label = tk.Label(self, text = help_text, font = ("tahoma", 8), fg = "gray")
            self.help_label.pack(anchor = "w", pady = (2, 0))
    
    def _update_value(self, event = None):
        self.value_label.config(text = f"{self.scale.get()} {self.unit}")
    
    def get_value(self):
        return self.scale.get()
    
    def set_value(self, value):
        self.scale.set(value)

class SliderWithEntry(tk.Frame):

    def __init__(self, master = None, label = "", from_ = 0, to = 100, unit="", help_text = None, **kwargs):
        super().__init__(master)
        self.from_ = from_
        self.to = to
        self.unit = unit

        # label
        if label:
            self.label = tk.Label(self, text = label)
            self.label.pack(anchor = "w")
        
        # slider frame
        self.inner_frame = tk.Frame(self)
        self.inner_frame.pack(fill = "x", expand = True)

        # slider scale
        self.value = tk.IntVar()
        self.scale = tk.Scale(
            self.inner_frame, from_ = self.from_, to = self.to,
            orient = "horizontal", variable = self.value, showvalue = False, **kwargs
        )
        self.scale.pack(side = "left", fill = "x", expand = True)

        # entry box
        validator = (self.register(validate_numeric), "%P")
        self.entry = tk.Entry(self.inner_frame, width = 6, justify = "center", validate = "key", validatecommand = validator)
        self.entry.pack(side = "left", padx = (5, 0))
        self.entry.insert(0, str(self.from_))

        # unit label
        if self.unit:
            self.unit_label = tk.Label(self.inner_frame, text = self.unit)
            self.unit_label.pack(side = "left", padx = (2, 0))

        # help text (if any)
        if help_text:
            self.help_label = tk.Label(self, text = help_text, font = ("tahoma", 8), fg = "gray")
            self.help_label.pack(anchor = "w", pady = (2, 0))
        
        # event bindings
        self.scale.bind("<B1-Motion>", self._update_entry_from_slider) # "<Motion>" causes hover bug that resets field to initial value on hover over sliders
        self.scale.bind("<ButtonRelease-1>", self._update_entry_from_slider)
        self.entry.bind("<Return>", self._update_slider_from_entry)
        self.entry.bind("<FocusOut>", self._update_slider_from_entry)
        self.entry.bind("<FocusIn>", show_touch_keyboard)

    def _update_entry_from_slider(self, event = None):
        value = self.value.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(value))

    def _update_slider_from_entry(self, event = None):
        try:
            value = int(self.entry.get())
        except ValueError:
            return # ignore for now, perhaps should show a warning message
        
        # clamp value range
        value = max(self.from_, min(self.to, value))
        self.value.set(value)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(value))

    def get_value(self):
        # if we clicked submit after typing in the entry field, 
        # the value doesn't get picked up as no event fires. do this to compensate
        self._update_slider_from_entry()
        return self.value.get()
    
    def set_value(self, value):
        self.value.set(value)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(value))