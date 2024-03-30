from unittest.mock import patch
import pytest
from app.plugins.calculations.divide import DivideCommand
from app.calculation_history import CalculationHistory
from app.logging_utility import LoggingUtility

@pytest.fixture
def mock_history_instance(mocker):
    mocker.patch.object(CalculationHistory, '__init__', return_value=None)
    history_instance = CalculationHistory()
    history_instance.add_record = mocker.MagicMock()
    return history_instance

@pytest.fixture
def divide_command(mock_history_instance):
    with patch('app.command.base_command.CalculationHistory', return_value=mock_history_instance):
        return DivideCommand()

def test_divide_command_success(divide_command, mocker):
    mock_info = mocker.patch.object(LoggingUtility, 'info')

    divide_command.execute('4', '2')

    mock_info.assert_called_once_with(2.0)
    divide_command.history_instance.add_record.assert_called_once()

def test_divide_command_invalid_input(divide_command, mocker):
    mock_error = mocker.patch.object(LoggingUtility, 'error')

    divide_command.execute('a', 'b')

    mock_error.assert_called_once_with("Error: All arguments must be numbers.")
    divide_command.history_instance.add_record.assert_not_called()

def test_divide_command_division_by_zero(divide_command, mocker):
    mock_error = mocker.patch.object(LoggingUtility, 'error')

    divide_command.execute('4', '0')

    mock_error.assert_called_once_with("Error: Cannot divide by zero.")
    divide_command.history_instance.add_record.assert_not_called()

def test_divide_command_incorrect_argument_count(divide_command, mocker):
    mock_warning = mocker.patch.object(LoggingUtility, 'warning')

    divide_command.execute('4')

    mock_warning.assert_called_once_with("Error: There can only be 2 arguments.")
    divide_command.history_instance.add_record.assert_not_called()