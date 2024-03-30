from unittest.mock import patch
import pytest
from app.plugins.history.delete import DeleteCommand
from app.calculation_history import CalculationHistory
from app.logging_utility import LoggingUtility

@pytest.fixture
def mock_history_instance(mocker):
    # Mock the CalculationHistory's constructor and delete_history method
    mocker.patch.object(CalculationHistory, '__init__', return_value=None)
    history_instance = CalculationHistory()
    history_instance.delete_history = mocker.MagicMock(return_value=True)
    return history_instance

@pytest.fixture
def delete_command(mock_history_instance):
    # Patch the CalculationHistory within DeleteCommand to use the mocked instance
    with patch('app.command.base_command.CalculationHistory', return_value=mock_history_instance):
        return DeleteCommand()

def test_delete_command_no_index_provided(delete_command, mocker):
    mock_warning = mocker.patch.object(LoggingUtility, 'warning')
    delete_command.execute()
    mock_warning.assert_called_once_with("You have to declare an index after the delete command.")

def test_delete_command_multiple_indices_provided(delete_command, mocker):
    mock_warning = mocker.patch.object(LoggingUtility, 'warning')
    delete_command.execute('1', '2')
    mock_warning.assert_called_once_with("You can declare only one index after the delete command.")

def test_delete_command_invalid_index(delete_command, mocker):
    mock_error = mocker.patch.object(LoggingUtility, 'error')
    delete_command.execute('a')
    mock_error.assert_called_once_with("Error: Index must be an integer.")

def test_delete_command_success(delete_command, mocker):
    mock_info = mocker.patch.object(LoggingUtility, 'info')
    delete_command.history_instance.delete_history.return_value = True
    delete_command.execute('1')
    delete_command.history_instance.delete_history.assert_called_once_with(0)  # Because we adjust index to be 0-based
    mock_info.assert_called_once_with('Record deleted.')  # Update to expect the call