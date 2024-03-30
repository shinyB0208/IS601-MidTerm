from abc import ABC, abstractmethod
from app.logging_utility import LoggingUtility

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    def execute_command(self, command_name, *args):
        #"Easier to Ask for Forgiveness than Permission" (EAFP)
        #As there are multiple ways an error can occur, so try catch is used
        try:
            # Execute the command with any arguments provided
            command = self.commands[command_name]
            result = command.execute(*args)  # Unpack arguments to pass to execute
            if result is not None:
                LoggingUtility.info(result)  # Or handle the command result as needed
        except KeyError:
            LoggingUtility.error(f"No such command: {command_name}")
        except Exception as e:
            LoggingUtility.error(f"Error executing command '{command_name}': {e}")