from unittest.mock import patch
import pytest
from app.plugins.calculations.multiply import MultiplyCommand
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
def multiply_command(mock_history_instance):
    # Patch the CalculationHistory within MultiplyCommand to use the mocked instance
    with patch('app.command.base_command.CalculationHistory', return_value=mock_history_instance):
        return MultiplyCommand()

def test_multiply_command_success(multiply_command, mocker):
    # Mock LoggingUtility.info to verify it's called correctly
    mock_info = mocker.patch.object(LoggingUtility, 'info')

    multiply_command.execute('2', '3')

    mock_info.assert_called_once_with(6.0)
    multiply_command.history_instance.add_record.assert_called_once()

def test_multiply_command_invalid_input(multiply_command, mocker):
    # Mock LoggingUtility.error to check for correct error handling
    mock_error = mocker.patch.object(LoggingUtility, 'error')

    multiply_command.execute('2', 'a')

    mock_error.assert_called_once_with("Error: All arguments must be numbers.")
    multiply_command.history_instance.add_record.assert_not_called()