from unittest.mock import MagicMock, patch
import pytest
from app.command import CommandHandler, Command
from app.logging_utility import LoggingUtility

# Mocking the abstract Command class for testing
class MockCommand(Command):
    def execute(self, *args):
        pass

@pytest.fixture
def command_handler():
    return CommandHandler()

@pytest.fixture
def mock_command():
    return MagicMock(spec=MockCommand)

def test_register_command(command_handler, mock_command):
    command_name = "test_command"
    command_handler.register_command(command_name, mock_command)
    assert command_name in command_handler.commands
    assert command_handler.commands[command_name] == mock_command

def test_execute_known_command(command_handler, mock_command):
    command_name = "test_command"
    mock_args = ('arg1', 'arg2')
    command_handler.register_command(command_name, mock_command)
    
    with patch.object(LoggingUtility, 'info') as mock_info:
        command_handler.execute_command(command_name, *mock_args)
        mock_command.execute.assert_called_once_with(*mock_args)
        mock_info.assert_called_once() 

def test_execute_unknown_command(command_handler):
    unknown_command_name = "unknown_command"
    
    with patch.object(LoggingUtility, 'error') as mock_error:
        command_handler.execute_command(unknown_command_name)
        mock_error.assert_called_once_with(f"No such command: {unknown_command_name}")

def test_execute_command_error_handling(command_handler, mock_command):
    command_name = "test_command"
    command_handler.register_command(command_name, mock_command)
    mock_command.execute.side_effect = Exception("Test exception")

    with patch.object(LoggingUtility, 'error') as mock_error:
        command_handler.execute_command(command_name)
        mock_error.assert_called_once_with(f"Error executing command '{command_name}': Test exception")