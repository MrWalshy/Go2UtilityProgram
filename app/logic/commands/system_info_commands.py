from logic.sys_info import get_system_info, get_cpu_info, get_battery_discharge_rate
from logic.commands.command import Command, CommandError

class SysInfoGetCommand(Command):

    def __init__(self, fn: callable, default_value = None):
        self._fn = fn
        self._value = default_value
    
    def execute(self):
        value = self._fn()
        if value is None:
            raise CommandError(f"[SysInfo Command]: Could not get {self._flag}")
        self._value = value
    
    @property
    def value(self):
        return self._value
    
class GetSystemInfo(SysInfoGetCommand):
    def __init__(self):
        super().__init__(fn = get_system_info)

class GetCpuInfo(SysInfoGetCommand):
    def __init__(self):
        super().__init__(fn = get_cpu_info)

class GetBatteryDischargeRate(SysInfoGetCommand):
    def __init__(self):
        super().__init__(fn = get_battery_discharge_rate)