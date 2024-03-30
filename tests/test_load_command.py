from unittest.mock import patch, MagicMock
import pytest
from pandas import DataFrame
from app.plugins.history.load import LoadCommand
from app.calculation_history import CalculationHistory
from app.logging_utility import LoggingUtility

@pytest.fixture
def mock_history_instance(mocker):
    # Mock the CalculationHistory's methods
    mocker.patch.object(CalculationHistory, '__init__', return_value=None)
    history_instance = CalculationHistory()
    history_instance.load_history = mocker.MagicMock()
    history_instance.history_df = MagicMock()
    return history_instance

@pytest.fixture
def load_command(mock_history_instance):
    # Use the mocked CalculationHistory instance in LoadCommand
    with patch('app.command.base_command.CalculationHistory', return_value=mock_history_instance):
        return LoadCommand()

def test_load_command_with_data(load_command, mocker):
    # Mock LoggingUtility.info
    mock_info = mocker.patch.object(LoggingUtility, 'info')
    
    # Setup mock history DataFrame
    data = {'Calculations': ['1 + 1 = 2', '2 * 3 = 6']}
    df = DataFrame(data)
    load_command.history_instance.history_df = df
    load_command.history_instance.load_history.return_value = True
    
    # Execute
    load_command.execute()
    
    # Verify LoggingUtility.info was called with the DataFrame's string representation
    mock_info.assert_called_once()
    assert df.to_string(index=False) in mock_info.call_args[0][0]

def test_load_command_empty(mock_history_instance, load_command, mocker):
    # Mock LoggingUtility.warning
    mock_warning = mocker.patch.object(LoggingUtility, 'warning')
    
    # Setup an empty DataFrame
    load_command.history_instance.history_df = DataFrame()
    load_command.history_instance.load_history.return_value = True
    
    # Execute
    load_command.execute()
    
    # Verify LoggingUtility.warning was called with "No calculations in history."
    mock_warning.assert_called_once_with("No calculations in history.")

def test_load_command_no_csv(load_command, mocker):
    # Mock LoggingUtility.warning
    mock_warning = mocker.patch.object(LoggingUtility, 'warning')
    
    # Setup load_history to return False (CSV not found)
    load_command.history_instance.load_history.return_value = False
    
    # Execute
    load_command.execute()
    
    # Verify LoggingUtility.warning was called with "Unable to load history. No CSV file present."
    mock_warning.assert_called_once_with("Unable to load history. No CSV file present.")