class Error(Exception):
    
    def __init__(self, code: int):
        self._code = code
    
    @property
    def code(self) -> int:
        return self._code
    
    def __str__(self) -> str:
        return repr(self._code)