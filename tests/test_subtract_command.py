from unittest.mock import patch
import pytest
from app.plugins.calculations.subtract import SubtractCommand
from app.calculation_history import CalculationHistory
from app.logging_utility import LoggingUtility

@pytest.fixture
def mock_history_instance(mocker):
    # Mock the CalculationHistory's constructor and add_record method
    mocker.patch.object(CalculationHistory, '__init__', return_value=None)
    history_instance = CalculationHistory()
    history_instance.add_record = mocker.MagicMock()
    return history_instance

@pytest.fixture
def subtract_command(mock_history_instance):
    # Patch the CalculationHistory within SubtractCommand to use the mocked instance
    with patch('app.command.base_command.CalculationHistory', return_value=mock_history_instance):
        return SubtractCommand()

def test_subtract_command_success(subtract_command, mocker):
    # Mock LoggingUtility.info to verify successful subtraction logs
    mock_info = mocker.patch.object(LoggingUtility, 'info')

    subtract_command.execute('5', '2', '1')

    mock_info.assert_called_once_with(2.0)  # 5 - 2 - 1 = 2
    subtract_command.history_instance.add_record.assert_called_once()

def test_subtract_command_invalid_input(subtract_command, mocker):
    # Mock LoggingUtility.error for invalid input error handling
    mock_error = mocker.patch.object(LoggingUtility, 'error')

    subtract_command.execute('5', 'two')

    mock_error.assert_called_once_with("Error: All arguments must be numbers.")
    subtract_command.history_instance.add_record.assert_not_called()

def test_subtract_command_single_input(subtract_command, mocker):
    # Test for single input, which should technically do nothing but return the number itself
    mock_info = mocker.patch.object(LoggingUtility, 'info')

    subtract_command.execute('3')

    mock_info.assert_called_once_with(3.0)
    subtract_command.history_instance.add_record.assert_called_once()