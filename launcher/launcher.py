import os, sys, subprocess

def main():
    # path to Python interpreter and entry script
    python_exe = os.path.join(os.path.dirname(sys.executable), "runtime", "python.exe")
    app_entry_point = os.path.join(os.path.dirname(sys.executable), "app", "app.py")

    if not os.path.exists(python_exe):
        print("Error: Python runtime not found at", python_exe)
        sys.exit(1)

    if not os.path.exists(app_entry_point):
        print("Error: App entry script not found at", app_entry_point)
        sys.exit(1)

    cmd = [python_exe, app_entry_point]
    os.execv(python_exe, cmd)

if __name__ == "__main__":
    main()