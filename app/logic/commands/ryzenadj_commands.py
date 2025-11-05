from logic.commands.command import Command, CommandError
from logic.ryzenadj.ryzenadj_wrapper import get as rz_get

class RyzenAdjGetCommand(Command):

    def __init__(self, flag: str, default_value = None):
        self._flag = flag
        self._value = default_value
    
    def execute(self):
        value = rz_get(self._flag)
        if value is None:
            raise CommandError(f"[RyzenAdj Command]: Could not get {self._flag}")
        self._value = value
    
    @property
    def value(self):
        return self._value

class GetStapmLimit(RyzenAdjGetCommand):
    def __init__(self):
        super().__init__(flag = "stapm_limit", default_value = -1)
    
class GetFastLimit(RyzenAdjGetCommand):
    def __init__(self):
        super().__init__(flag = "fast_limit", default_value = -1)

class GetSlowLimit(RyzenAdjGetCommand):
    def __init__(self):
        super().__init__(flag = "slow_limit", default_value = -1)

class GetStapmValue(RyzenAdjGetCommand):
    def __init__(self):
        super().__init__(flag = "stapm_value", default_value = -1)

class GetFastValue(RyzenAdjGetCommand):
    def __init__(self):
        super().__init__(flag = "fast_value", default_value = -1)

class GetSlowValue(RyzenAdjGetCommand):
    def __init__(self):
        super().__init__(flag = "slow_value", default_value = -1)