from unittest.mock import patch
import pytest
from app.plugins.history.clear import ClearCommand
from app.calculation_history import CalculationHistory
from app.logging_utility import LoggingUtility

@pytest.fixture
def mock_history_instance(mocker):
    # Mock the CalculationHistory's constructor and clear_history method
    mocker.patch.object(CalculationHistory, '__init__', return_value=None)
    history_instance = CalculationHistory()
    history_instance.clear_history = mocker.MagicMock()
    return history_instance

@pytest.fixture
def clear_command(mock_history_instance):
    # Patch the CalculationHistory within ClearCommand to use the mocked instance
    with patch('app.command.base_command.CalculationHistory', return_value=mock_history_instance):
        return ClearCommand()

def test_clear_command_success(clear_command, mocker):
    # Mock LoggingUtility.info to verify successful history clearance logs
    mock_info = mocker.patch.object(LoggingUtility, 'info')

    clear_command.execute()

    mock_info.assert_called_once_with("Calculation history cleared.")
    clear_command.history_instance.clear_history.assert_called_once()

def test_clear_command_with_arguments(clear_command, mocker):
    # Mock LoggingUtility.warning to check for the warning when arguments are passed
    mock_warning = mocker.patch.object(LoggingUtility, 'warning')

    clear_command.execute('unexpected_argument')

    mock_warning.assert_called_once_with("The clear command does not accept any arguments.")
    clear_command.history_instance.clear_history.assert_not_called()