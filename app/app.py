import ctypes
import sys
import os
import subprocess
from tkinter import messagebox

CONFIG_FILE = os.path.join(os.getenv("APPDATA"), "Go2Utility", "config.txt")

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

def unhide_power_settings():
    """Unhides all power settings in the power plans (requires admin).
    
    https://gist.github.com/Velocet/7ded4cd2f7e8c5fa475b8043b76561b5
    """
    ps_command = r"(gci 'HKLM:\SYSTEM\CurrentControlSet\Control\Power\PowerSettings' -Recurse).Name -notmatch '\bDefaultPowerSchemeValues|(\\[0-9]|\b255)$' | % {sp $_.Replace('HKEY_LOCAL_MACHINE','HKLM:') -Name 'Attributes' -Value 2 -Force}"
    print(f"Running: {ps_command}")
    subprocess.run(["powershell", "-Command", ps_command], check = True, shell = True)

def has_run_before() -> bool:
    return os.path.exists(CONFIG_FILE)

def mark_as_run_before():
    with open(CONFIG_FILE, "w") as file:
        file.write("power_settings_unlocked = True\n")

def ensure_config_folder_exists():
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok = True)

def run_first_time_setup():
    ensure_config_folder_exists()
    if not has_run_before():
        if messagebox.askyesno(
            "Unlock Advanced Power Settings",
            "As this is the first time you have launched the app, we need to unhide hidden power plan settings so the values can be read by the app.\n Would you like to unlock all hidden power plan options? (Requires admin privileges)"
        ):
            try:
                unhide_power_settings()
                mark_as_run_before()
                messagebox.showinfo("Done!", "Please restart the app.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to unlock power settings:\n{e}")

if __name__ == "__main__":
    run_as_admin()
    run_first_time_setup()

    try:
        from logic.sys_info import test
        from logic.ryzenadj.ryzenadj_wrapper import test_get
        test()
        test_get()
        
        from gui.window import Window
        from gui.pages.processor_settings import ProcessorSettingsPage
        from gui.pages.power_settings import PowerSettingsPage

        window = Window(pages = [
            (ProcessorSettingsPage, "Processor performance settings"),
            (PowerSettingsPage, "Power settings")
        ])
        window.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Press enter to exit...")


