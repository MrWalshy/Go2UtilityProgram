from abc import ABC, abstractmethod
from typing import List
from error import Error

class Command(ABC):
    """Abstract base class for command classes."""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass

class CompositeCommand(Command):
    """Base class for executing multiple commands in a row."""

    def __init__(self, commands: List[Command]):
        self._commands = commands
    
    def execute(self) -> None:
        for command in self._commands:
            command.execute()

class ReversibleCommand(Command):

    @abstractmethod
    def undo(self) -> None:
        """Undo the executed command."""
        pass

class ReversibleCompositeCommand(ReversibleCommand):
    """Base class for executing multiple commands in a row."""

    def __init__(self, commands: List[ReversibleCommand]):
        self._commands = commands
    
    def execute(self) -> None:
        for command in self._commands:
            command.execute()
    
    def undo(self) -> None:
        """Undo the composite command, operates in reverse order to execute."""
        for command in reversed(self._commands):
            command.undo()

class CommandError(Error):

    def __init__(self, message: str):
        super().__init__(1000)
        self.message = message
    
    def __str__(self):
        return f"{self.get_code()}: {self.message}"