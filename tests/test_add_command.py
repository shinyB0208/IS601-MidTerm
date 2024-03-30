from unittest.mock import patch
import pytest
from app.plugins.calculations.add import AddCommand
from app.calculation_history import CalculationHistory
from app.logging_utility import LoggingUtility

@pytest.fixture
def mock_history_instance(mocker):
    # Mock the CalculationHistory instance
    mocker.patch.object(CalculationHistory, '__init__', return_value=None)
    history_instance = CalculationHistory()
    history_instance.add_record = mocker.MagicMock()
    return history_instance

@pytest.fixture
def add_command(mock_history_instance):
    # Use the mocked CalculationHistory instance in AddCommand
    with patch('app.command.base_command.CalculationHistory', return_value=mock_history_instance):
        return AddCommand()

def test_add_command_success(add_command, mocker):
    # Mock the LoggingUtility
    mock_info = mocker.patch.object(LoggingUtility, 'info')

    # Execute the command with valid numeric arguments
    add_command.execute('1', '2')

    # Assertions
    mock_info.assert_called_once_with(3)
    add_command.history_instance.add_record.assert_called_once()

def test_add_command_value_error(add_command, mocker):
    # Mock the LoggingUtility
    mock_error = mocker.patch.object(LoggingUtility, 'error')

    # Execute the command with at least one non-numeric argument
    add_command.execute('1', 'a')

    # Assertions
    mock_error.assert_called_once_with("Error: All arguments must be numbers.")
    add_command.history_instance.add_record.assert_not_called()