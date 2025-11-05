import tkinter as tk
from tkinter import ttk
from typing import List, Tuple
from gui.pages.page import Page

class Window(tk.Tk):

    def __init__(self, pages: List[Tuple[Page, str]]):
        '''Pages takes the form: [(PageClass, name), ...]'''
        super().__init__()
        self.title("Go 2 Options")
        #self.geometry("1600x1000") # 1000p

        # layout
        self.navbar = ttk.Frame(self)
        self.navbar.pack(side = "left", fill = "y")
        self.container = ttk.Frame(self)
        self.container.pack(side = "left", fill = "both", expand = True)

        # allow the content to grow to fit remaining frame width, weight param allows this
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        # page load
        self.pages = {}
        for PageClass, name in pages:
            frame = PageClass(master = self.container)
            self.pages[name] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        
        # nav buttons
        for page_name, page in self.pages.items():
            ttk.Button(
                self.navbar, text = page_name, 
                command = lambda name = page_name: self.show_page(name)
            ).pack(fill = "x", pady = 5)
        
        page_names = [key for key, _ in self.pages.items()]
        self.current_page = None
        self.show_page(page_names[0])
    
    def show_page(self, page_name: str) -> None:
        if self.current_page == page_name:
            return
        
        print(f"Opening page: {page_name}")
        # hide the current page
        if self.current_page != None:
            self.pages[self.current_page].on_hide()

        frame = self.pages[page_name]
        frame.tkraise()
        self.current_page = page_name

        # show new page
        frame.on_show()