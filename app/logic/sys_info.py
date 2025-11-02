import psutil
import platform
import wmi # Windows Management Instrumentation

uname = platform.uname()
wmi_root = wmi.WMI(namespace = "root\\wmi")

def get_system_info():
    return {
        "system": uname.system,
        "processor": uname.processor,
        "version": uname.version,
        "machine": uname.machine,
    }

def get_cpu_info():
    cpu_frequency = psutil.cpu_freq()
    return {
        "cores": psutil.cpu_count(logical = False),
        "logical_cores": psutil.cpu_count(logical = True),
        "max_frequency": cpu_frequency.max,
        "min_frequency": cpu_frequency.min,
        "current_frequency": cpu_frequency.current
    }

def get_battery_discharge_rate():
    try:
        status = wmi_root.BatteryStatus()[0]
        # discharge rate in mW
        discharge_mw = status.DischargeRate
        # < 0 means it is discharging, otherwise its charging
        return discharge_mw
    except IndexError:
        print("No battery")
    except Exception as e:
        print(f"Error reading battery discharge rate: {e}")
    return None

def get_current_package_power_draw():
    pass

def test():
    sys_info = get_system_info()
    cpu_info = get_cpu_info()
    discharge_rate = get_battery_discharge_rate()

    for key, value in sys_info.items():
        print(f"{key}: {value}")
    for key, value in cpu_info.items():
        print(f"{key}: {value}")
    print(f"Battery Discharge Rate: {discharge_rate}")