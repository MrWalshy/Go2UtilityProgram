import ctypes
import sys
import os

def run_as_admin():
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if not is_admin:
        script = sys.executable
        params = " ".join(f'"{arg}"' for arg in sys.argv)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", script, params, None, 1
        )
        sys.exit()

if __name__ == "__main__":
    run_as_admin()

    try:
        from gui.form import OptionsForm
        import tkinter as tk
        root = tk.Tk()
        root.title("Go 2 Options")
        OptionsForm(master = root)
        root.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Press enter to exit...")


