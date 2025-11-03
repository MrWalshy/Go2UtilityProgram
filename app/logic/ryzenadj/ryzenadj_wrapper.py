import os, sys, time
import ctypes
from ctypes import c_double, c_uint32, c_char_p, c_void_p, c_float, c_ulong, byref, POINTER, cdll
from shutil import copyfile

# script_dir = os.path.dirname(os.path.abspath(__file__))
# lib_path = script_dir
# dll_path = os.path.join(script_dir, "libryzenadj.dll")
# ryzenadj = ctypes.CDLL(dll_path)

if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable) # pyinstaller exe
else:
    base_dir = os.path.dirname(os.path.abspath(__file__)) # running from script

######## if i don't include this, the script shits itself for some reason and won't init ryzenadj
os.chdir(base_dir)
if sys.platform == 'win32' or sys.platform == 'cygwin':
    try:
        os.add_dll_directory(base_dir)
    except AttributeError:
        pass #not needed for old python version

    winring0_driver_file_path = os.path.join(os.path.dirname(base_dir), 'WinRing0x64.sys')
    if not os.path.isfile(winring0_driver_file_path):
        copyfile(os.path.join(base_dir, 'WinRing0x64.sys'), winring0_driver_file_path)

    ryzenadj = cdll.LoadLibrary('libryzenadj')
else:
    ryzenadj = cdll.LoadLibrary('libryzenadj.so')
########

##### cannot access memory??? when running gets
# if getattr(sys, 'frozen', False):
#     base_dir = os.path.dirname(sys.executable) # pyinstaller exe
# else:
#     base_dir = os.path.dirname(os.path.abspath(__file__)) # running from script

# dll_path = os.path.join(base_dir, "libryzenadj.dll")
# winring_dll_path = os.path.join(base_dir, "WinRing0x64")
# winring_sys_path = os.path.join(base_dir, "WinRing0x64.sys")

# exe_sys_path = os.path.join(base_dir, "WinRing0x64.sys")
# if not os.path.isfile(exe_sys_path):
#     copyfile(winring_sys_path, exe_sys_path)
#####
#ryzenadj = cdll.LoadLibrary(dll_path)

# ctype mappings (function args and return types?)
ryzenadj.init_ryzenadj.restype = c_void_p
ryzenadj.get_table_ver.argtypes = [c_void_p]
ryzenadj.get_table_size.argtypes = [c_void_p]
ryzenadj.get_table_values.restype = POINTER(c_float)
ryzenadj.get_table_values.argtypes = [c_void_p]
ryzenadj.refresh_table.argtypes = [c_void_p]
ryzenadj.get_fast_limit.restype = c_float
ryzenadj.get_fast_limit.argtypes = [c_void_p]

ry = ryzenadj.init_ryzenadj() # get handle to the SMU?

if not ry:
    print("RyzenAdj could not get initialized")

error_messages = {
    -1: "{:s} is not supported on this family\n",
    -3: "{:s} is not supported on this SMU\n",
    -4: "{:s} is rejected by SMU\n"
}

setter_fields = {
    "stapm_limit": "Sustained PPT limit (mW, 10W = 10000mW)",
    "fast_limit": "Fast PPT limit (mW, 10W = 10000mW)",
    "slow_limit": "Slow PPT limit (mW, 10W = 10000mW)",
    "min_gfxclk": "Minimum graphics clock (Hz/MHz/GHz?)",
    "max_gfxclk": "Minimum graphics clock (Hz/MHz/GHz?)",
    "gfxclk": "Minimum graphics clock (Hz/MHz/GHz?)"
}

getter_fields = {
    "stapm_limit": "Sustained PPT limit (mW, 10W = 10000mW)",
    "fast_limit": "Fast PPT limit (mW, 10W = 10000mW)",
    "slow_limit": "Slow PPT limit (mW, 10W = 10000mW)",
    "gfxclk": "Graphics clock (Hz/MHz/GHz?)",
    "soc_power": "SoC power draw (imc and other bits)",
    "socket_power": "Total package power (cores, cache, SoC, etc...)"
}


def is_ryzenadj_initialised() -> bool:
    if not ry:
        return False
    return True

# fields:
# - stapm_limit
# - fast_limit
# - slow_limit
# - min_gfxclk, max_gfxclk, gfx_clk (will need to test if these work on Z2E and what units they take)
def adjust(field, value): # (str, int32)
    if not ry:
        return
    
    function_name = "set_" + field
    adjust_func = ryzenadj.__getattr__(function_name) # dynamically looks up the function
    adjust_func.argtypes = [c_void_p, c_ulong] # struct handle (ry), value arg
    res = adjust_func(ry, value)
    if res:
        error = error_messages.get(res, "{:s} did fail with {:d}\n")
        print(error.format(function_name, res));

def enable(field):
    if not ry:
        return
    
    function_name = "set_" + field
    adjust_func = ryzenadj.__getattr__(function_name)
    adjust_func.argtypes = [c_void_p]
    res = adjust_func(ry)
    if res:
        error = error_messages.get(res, "{:s} did fail with {:d}\n")
        print(error.format(function_name, res));

# fields:
# - stapm_limit, stapm_value
# - fast_limit, slow_limit, fast_value, slow_value
# - core_clk, core_volt, core_power, core_temp
# - gfx_clk, gfx_temp, gfx_volt
# - mem_clk, fclk
# - soc_power, soc_volt
# - socket_power
def get(field):
    function_name = "get_" + field
    try:
        get_func = ryzenadj.__getattr__(function_name)
    except AttributeError:
        print(f"{function_name} not found in libryzenadj.dll\n")
        return None
    
    ryzenadj.refresh_table(ry) # need to do this to make sure ryzenadj has read in the data, otherwise I just get nan

    get_func.argtypes = [c_void_p] # just the struct handle (ry: ryzen_access)
    get_func.restype = c_float # response type: EXP float CALL get_stapm_limit(ryzen_access ry);
    
    try:
        value = get_func(ry)
        return value
    except Exception as e:
        #sys.stderr.write(f"{function_name} failed: {e}\n")
        print(f"{function_name} failed: {e}\n")
        return None

# get func just tells me memory cannot be accessed, will just try what is in the example script to check for diff response
print("pmtable version: {:x}".format(ryzenadj.get_table_ver(ry)))

#input("Press any key to show all pmtable values...")

pmtable_size = ryzenadj.get_table_size(ry) // 4
pmtable = ryzenadj.get_table_values(ry)

def test_get():
    ryzenadj.refresh_table(ry)
    columns, lines = os.get_terminal_size()
    table_columns = columns // 16 # 16 chars per table entry
    #os.system('cls' if sys.platform == 'win32' else 'clear')
    table_rows = 0
    for index in (range(pmtable_size)):
        print("{:3d}:{:8.2f}\t".format(index, pmtable[index]))
        if index % table_columns == table_columns - 1: 
            print('\n')
            table_rows += 1
            if table_rows >= lines - 1:
                print('{:d} More entries ...'.format(pmtable_size - 1 - index))
                break
    
    #if index % table_columns != table_columns - 1: print('\n')
    #sys.stdout.flush()
    #time.sleep(1)
    # this tells me the memory cannot be accessed? WHYYYYYYY?
    for func, description in getter_fields.items():
        print(f"Attempting get for {func}: {description}")
        value = get(func)
        print(f"  Received: {value}")

    # let's see if trying to manually call the stapm function works
    get_func = ryzenadj.get_stapm_limit
    get_func.argtypes = [c_void_p]
    get_func.restype = c_float
    value = get_func(ry)
    print("STAPM limit:", value)