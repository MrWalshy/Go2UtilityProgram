import subprocess
import re

subgroups = {
    "PROCESSOR_POWER_MANAGEMENT": {
        "GUID": "54533251-82be-4824-96c1-47b60b740d00",
        "ALIAS": "SUB_PROCESSOR"
    }
}

options = {
    "EPP_E_CORE": {
        "GUID": "36687f9e-e3a5-4dbf-b1dc-15eb381c6863",
        "ALIAS": "PERFEPP"
    },
    "EPP_P_CORE": {
        "GUID": "36687f9e-e3a5-4dbf-b1dc-15eb381c6864",
        "ALIAS": "PERFEPP1"
    },
    "MAX_E_CORE_FREQ": {
        "GUID": "75b0ae3f-bce0-45a7-8c89-c9611c25e100",
        "ALIAS": "PROCFREQMAX"
    },
    "MAX_P_CORE_FREQ": {
        "GUID": "75b0ae3f-bce0-45a7-8c89-c9611c25e101",
        "ALIAS": "PROCFREQMAX1"
    },
    "PROCESSOR_PERFORMANCE_BOOST_MODE": {
        "GUID": "be337238-0d82-4146-a960-4f3749d470c7",
        "ALIAS": "PERFBOOSTMODE",
        "OPTIONS": {
            "DISABLED": 0,
            "ENABLED": 1,
            "AGGRESSIVE": 2,
            "EFFICIENT_ENABLED": 3,
            "EFFICIENT_AGGRESSIVE": 4
        }
    }
}

def get_active_power_scheme():
    '''Return the GUID of the current power plan scheme'''
    result = subprocess.run(["powercfg", "/getactivescheme"], capture_output = True, text = True)
    match = re.search(r"GUID:\s*([a-f0-9\-]+)", result.stdout, re.I)
    return match.group(1) if match else None

def set_plan_setting(power_scheme, subgroup, setting, value):
    cmd_ac = [
        "powercfg", "/setacvalueindex",
        power_scheme, subgroup, setting, str(value)
    ]
    cmd_dc = [
        "powercfg", "/setdcvalueindex",
        power_scheme, subgroup, setting, str(value)
    ]
    print("power_scheme =", power_scheme, type(power_scheme))
    print("subgroup =", subgroup, type(subgroup))
    print("setting =", setting, type(setting))
    print("value =", value, type(value))
    subprocess.run(cmd_ac, check = True)
    subprocess.run(cmd_dc, check = True)
    # force power plan reload to ensure values actually take effect
    subprocess.run(["powercfg", "/setactive", power_scheme], check = True)

def set_p_core_limit(power_scheme_guid, mhz = -1):
    if mhz == -1:
        return
    print("Setting P core limit")
    set_plan_setting(
        power_scheme_guid, subgroups["PROCESSOR_POWER_MANAGEMENT"]["GUID"],
        options["MAX_P_CORE_FREQ"]["GUID"],
        mhz
    )

def set_e_core_limit(power_scheme_guid, mhz = -1):
    if mhz == -1:
        return
    print("Setting E core limit")
    set_plan_setting(
        power_scheme_guid, subgroups["PROCESSOR_POWER_MANAGEMENT"]["GUID"],
        options["MAX_E_CORE_FREQ"]["GUID"],
        mhz
    )
    

def set_cpu_boost_mode(power_scheme_guid, mode = ""):
    if mode == "":
        return
    print(f"Setting CPU boost mode: {mode}")
    value = 0 if mode == "Disabled" else 1
    set_plan_setting(
        power_scheme_guid, subgroups["PROCESSOR_POWER_MANAGEMENT"]["GUID"],
        options["PROCESSOR_PERFORMANCE_BOOST_MODE"]["GUID"],
        value
    )

def set_energy_performance_preference(power_scheme_guid, percentage = 0):
    print(f"Setting CPU EPP to: {percentage}%")
    set_plan_setting(
        power_scheme_guid, subgroups["PROCESSOR_POWER_MANAGEMENT"]["GUID"],
        options["EPP_P_CORE"]["GUID"],
        percentage
    )
    set_plan_setting(
        power_scheme_guid, subgroups["PROCESSOR_POWER_MANAGEMENT"]["GUID"],
        options["EPP_E_CORE"]["GUID"],
        percentage
    )